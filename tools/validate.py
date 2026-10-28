#!/usr/bin/env python3
"""Validate this project's declared schema subset and evidence semantics.

This is not a general JSON Schema 2020-12 implementation. It implements every
keyword used in the two published project schemas, plus project-specific checks.
"""
import argparse
import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def is_type(value, kind):
    return {'object': lambda: isinstance(value, dict),
            'array': lambda: isinstance(value, list),
            'string': lambda: isinstance(value, str),
            'number': lambda: isinstance(value, (int, float)) and not isinstance(value, bool),
            'null': lambda: value is None}[kind]()


def schema_check(value, schema, root, path, errors):
    if '$ref' in schema:
        target = root
        for key in schema['$ref'].removeprefix('#/').split('/'):
            target = target[key]
        return schema_check(value, target, root, path, errors)
    kinds = schema.get('type')
    if kinds is not None:
        kinds = kinds if isinstance(kinds, list) else [kinds]
        if not any(is_type(value, kind) for kind in kinds):
            errors.append(f'{path}: invalid type; expected {kinds}')
            return
    if 'const' in schema and value != schema['const']:
        errors.append(f'{path}: invalid constant')
    if 'enum' in schema and value not in schema['enum']:
        errors.append(f'{path}: invalid enum value')
    if isinstance(value, str):
        if len(value.strip()) < schema.get('minLength', 0):
            errors.append(f'{path}: empty or too short')
        if 'pattern' in schema and re.search(schema['pattern'], value) is None:
            errors.append(f'{path}: invalid pattern')
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if not math.isfinite(value):
            errors.append(f'{path}: nonfinite number')
        if 'minimum' in schema and value < schema['minimum']:
            errors.append(f'{path}: below minimum')
    if isinstance(value, dict):
        for key in schema.get('required', []):
            if key not in value:
                errors.append(f'{path}.{key}: required field missing')
        for key, child in schema.get('properties', {}).items():
            if key in value:
                schema_check(value[key], child, root, f'{path}.{key}', errors)
    if isinstance(value, list) and 'items' in schema:
        for i, child in enumerate(value):
            schema_check(child, schema['items'], root, f'{path}[{i}]', errors)


def validate(root=ROOT, submission=False):
    errors = []
    try:
        def read(name):
            return json.loads((root / name).read_text(encoding='utf-8'), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(f'invalid constant {x}')))
        project, evidence = read('project.json'), read('evidence.json')
        for name, value in [('project', project), ('evidence', evidence)]:
            schema = read(f'schemas/{name}.schema.json')
            schema_check(value, schema, schema, name, errors)
        if errors:
            return errors
        source_map = {item['id']: item for item in evidence['sources']}
        observation_map = {item['id']: item for item in evidence['observations']}
        if set(project['source_ids']) != set(source_map):
            errors.append('project: source_ids must match defined sources')
        all_ids = [item['id'] for group in ('sources', 'observations', 'claims') for item in evidence[group]]
        if len(all_ids) != len(set(all_ids)):
            errors.append('evidence: duplicate IDs')
        for observation in evidence['observations']:
            source = source_map.get(observation['source_id'])
            if source is None:
                errors.append(f"{observation['id']}: dangling source")
            elif source['access_state'] == 'unread':
                errors.append(f"{observation['id']}: observation cites unread source")
        for claim in evidence['claims']:
            prefix = claim['id']
            if claim['kind'] == 'proposal' and claim['status'] != 'proposed':
                errors.append(f'{prefix}: proposal cannot be promoted to a completed finding')
            if claim['kind'] != 'proposal' and not claim['evidence_ids']:
                errors.append(f'{prefix}: non-proposal needs located evidence')
            cited = []
            for identifier in claim['evidence_ids']:
                if identifier not in observation_map:
                    errors.append(f'{prefix}: dangling observation {identifier}')
                else:
                    cited.append(observation_map[identifier])
            expected = {(o['source_id'], o['locator']) for o in cited}
            actual = {(o['source_id'], o['locator']) for o in claim['source_locators']}
            if expected != actual:
                errors.append(f'{prefix}: claim locators must match cited observations exactly')
        original_sources = [s for s in evidence['sources'] if s['kind'] == 'original_artifact']
        if not original_sources:
            errors.append('evidence: missing original artifact')
        states = {s['access_state'] for s in original_sources}
        if project['source_state'] == 'read' and states != {'read'}:
            errors.append('project: read status inconsistent with original sources')
        manifest = read('evidence/manifest.json')
        raw = (root / manifest['original_path']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != manifest['original_sha256']:
            errors.append('source: SHA-256 integrity mismatch')
        if len(raw) != manifest['original_bytes']:
            errors.append('source: byte length mismatch')
        normalized = raw.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
        numbered = ''.join(f'{i:03d} | {s}\n' for i, s in enumerate(normalized.splitlines(), 1))
        if (root / manifest['normalized_derivative']).read_text() != numbered:
            errors.append('source: numbered derivative is stale')
        if manifest['source_id'] not in source_map:
            errors.append('manifest: source ID missing from ledger')
        for o in evidence['observations']:
            if o['source_id'] == manifest['source_id']:
                if re.fullmatch(r'L\d+(?:-L?\d+)?(?:; L\d+(?:-L?\d+)?)*', o['locator']) is None:
                    errors.append(f"{o['id']}: original source needs a recognized line locator")
                for start, end in re.findall(r'L(\d+)(?:-L?(\d+))?', o['locator']):
                    last = int(end or start)
                    if int(start) < 1 or last < int(start) or last > len(normalized.splitlines()):
                        errors.append(f"{o['id']}: original source line range out of bounds")
        for field in ('activity_dates', 'hours', 'role', 'impact'):
            if project[field] is not None:
                ids = project.get('personal_field_evidence', {}).get(field, [])
                if not ids or any(i not in observation_map for i in ids):
                    errors.append(f'project.{field}: non-null personal fact needs observation IDs')
        if submission:
            if project['source_state'] != 'read':
                errors.append('submission: original source review incomplete')
            if project['student_verification'] != 'verified':
                errors.append('submission: student verification pending')
            if project['artifact_state'] != 'reviewed':
                errors.append('submission: artifact is still draft')
            verification = project.get('verification_evidence_ids', [])
            if not verification or any(i not in observation_map or source_map.get(observation_map[i]['source_id'], {}).get('kind') != 'student_record' for i in verification):
                errors.append('submission: no located student authorship/contribution verification record')
            for field in ('activity_dates', 'hours', 'role'):
                if project[field] is None:
                    errors.append(f'submission: {field} remains unverified')
    except (OSError, ValueError, KeyError, TypeError) as error:
        errors.append(f'input: {error}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--submission', action='store_true')
    args = parser.parse_args()
    errors = validate(submission=args.submission)
    if errors:
        print('\n'.join('FAIL: ' + e for e in errors))
        raise SystemExit(1)
    print('PASS: repository schema constraints, evidence links, and source integrity')
    if not args.submission:
        print('Draft validation is not student authorship verification or submission approval.')


if __name__ == '__main__':
    main()
