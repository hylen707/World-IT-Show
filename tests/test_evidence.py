"""Mutation tests for failure modes that could misrepresent evidence."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / f'{name}.py')
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


validate = module('validate').validate
calculate = module('analyze').calculate


class EvidenceMutationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for name in ['project.json', 'evidence.json', 'schemas', 'evidence']:
            src = ROOT / name
            if src.is_dir():
                shutil.copytree(src, self.root / name)
            else:
                shutil.copy2(src, self.root / name)

    def tearDown(self):
        self.tmp.cleanup()

    def mutate(self, name, change):
        path = self.root / name
        value = json.loads(path.read_text())
        change(value)
        path.write_text(json.dumps(value))

    def assert_rejected(self, text):
        self.assertTrue(any(text in error for error in validate(self.root)), validate(self.root))

    def test_current_draft_validates(self):
        self.assertEqual(validate(self.root), [])

    def test_missing_student_verification_blocks_submission(self):
        errors = validate(self.root, submission=True)
        self.assertTrue(any('student verification pending' in e for e in errors))

    def test_setting_verified_flag_alone_is_insufficient(self):
        self.mutate('project.json', lambda p: p.update(student_verification='verified', artifact_state='reviewed'))
        self.assertTrue(any('no located student' in e for e in validate(self.root, submission=True)))

    def test_unbacked_finding_is_rejected(self):
        self.mutate('evidence.json', lambda e: e['claims'][0].update(evidence_ids=[], source_locators=[]))
        self.assert_rejected('needs located evidence')

    def test_unknown_observation_is_rejected(self):
        self.mutate('evidence.json', lambda e: e['claims'][0].update(evidence_ids=['O999']))
        self.assert_rejected('dangling observation')

    def test_forged_locator_is_rejected(self):
        self.mutate('evidence.json', lambda e: e['claims'][0]['source_locators'][0].update(locator='L999'))
        self.assert_rejected('locators must match')

    def test_source_line_out_of_range_is_rejected(self):
        self.mutate('evidence.json', lambda e: e['observations'][0].update(locator='L999'))
        self.assert_rejected('line range out of bounds')

    def test_unrecognized_original_locator_is_rejected(self):
        self.mutate('evidence.json', lambda e: e['observations'][0].update(locator='nonsense'))
        self.assert_rejected('recognized line locator')

    def test_dangling_project_source_is_rejected(self):
        self.mutate('project.json', lambda p: p['source_ids'].append('S99'))
        self.assert_rejected('source_ids must match')

    def test_duplicate_ids_are_rejected(self):
        self.mutate('evidence.json', lambda e: e['observations'].append(copy.deepcopy(e['observations'][0])))
        self.assert_rejected('duplicate IDs')

    def test_wrong_evidence_field_type_is_rejected(self):
        self.mutate('evidence.json', lambda e: e['claims'][0].update(evidence_ids='O01'))
        self.assert_rejected('invalid type')

    def test_invalid_status_is_rejected(self):
        self.mutate('evidence.json', lambda e: e['claims'][0].update(status='proven'))
        self.assert_rejected('invalid enum')

    def test_unread_source_cannot_supply_observation(self):
        self.mutate('evidence.json', lambda e: e['sources'][0].update(access_state='unread'))
        self.assert_rejected('unread source')

    def test_proposal_cannot_be_completed_finding(self):
        self.mutate('evidence.json', lambda e: e['claims'][-1].update(status='supported'))
        self.assert_rejected('proposal cannot be promoted')

    def test_original_byte_tamper_is_detected(self):
        path = self.root / 'evidence/original.txt'
        path.write_bytes(path.read_bytes() + b'edited')
        self.assert_rejected('integrity mismatch')

    def test_stale_derived_source_is_detected(self):
        (self.root / 'evidence/source-numbered.txt').write_text('altered derivative')
        self.assert_rejected('derivative is stale')

    def test_invented_hours_need_evidence(self):
        self.mutate('project.json', lambda p: p.update(hours=100))
        self.assert_rejected('personal fact needs observation')

    def test_boolean_is_not_hours_number(self):
        self.mutate('project.json', lambda p: p.update(hours=True))
        self.assert_rejected('invalid type')


class ModelBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.inputs = json.loads((ROOT / 'analysis/model-inputs.json').read_text())

    def test_equal_task_efficiency_gives_equal_energy_for_different_power(self):
        runs = calculate(self.inputs)['thermal']['power_comparison']
        self.assertEqual(runs[0]['modeled_wall_energy_Wh'], runs[1]['modeled_wall_energy_Wh'])
        self.assertEqual(runs[0]['idealized_heating_time_seconds'], 2 * runs[1]['idealized_heating_time_seconds'])

    def test_lower_efficiency_can_increase_energy(self):
        run = calculate(self.inputs)['thermal']['scenarios'][0]
        self.assertLess(run['modeled_savings_vs_assumed_baseline_percent'], 0)

    def test_zero_efficiency_is_rejected(self):
        self.inputs['thermal']['assumed_task_efficiencies'] = [0]
        with self.assertRaises(ValueError):
            calculate(self.inputs)

    def test_superunit_efficiency_is_rejected(self):
        self.inputs['thermal']['assumed_task_efficiencies'] = [1.1]
        with self.assertRaises(ValueError):
            calculate(self.inputs)

    def test_nonfinite_input_is_rejected(self):
        self.inputs['area']['reported_m2_per_g'] = float('nan')
        with self.assertRaises(ValueError):
            calculate(self.inputs)


if __name__ == '__main__':
    unittest.main()
