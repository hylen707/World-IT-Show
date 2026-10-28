#!/usr/bin/env python3
"""Reproduce bounded, illustrative calculations; never product measurements."""
import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def positive(value, name, upper=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite positive number")
    if upper is not None and value > upper:
        raise ValueError(f"{name} must not exceed {upper}")
    return value


def calculate(inputs):
    area = inputs['area']
    claimed = positive(area['reported_m2_per_g'], 'reported area')
    reference = positive(area['ideal_two_face_m2_per_g'], 'reference area')
    load = inputs['thermal']
    mass = positive(load['assumed_mass_kg'], 'mass')
    heat_capacity = positive(load['assumed_heat_capacity_J_per_kg_K'], 'heat capacity')
    delta = positive(load['assumed_temperature_change_K'], 'temperature change')
    baseline = positive(load['assumed_baseline_task_efficiency'], 'baseline efficiency', 1)
    useful_j = mass * heat_capacity * delta
    useful_wh = useful_j / 3600
    scenarios = []
    for eta in load['assumed_task_efficiencies']:
        eta = positive(eta, 'scenario efficiency', 1)
        scenarios.append({'assumed_task_efficiency': eta,
                          'modeled_wall_energy_Wh': round(useful_wh / eta, 6),
                          'modeled_savings_vs_assumed_baseline_percent': round((1 - baseline / eta) * 100, 6)})
    powers = []
    for power in load['assumed_powers_W']:
        power = positive(power, 'power')
        powers.append({'assumed_power_W': power, 'assumed_task_efficiency': baseline,
                       'modeled_wall_energy_Wh': round(useful_wh / baseline, 6),
                       'idealized_heating_time_seconds': round(useful_j / (power * baseline), 6)})
    return {
        'interpretation': 'Illustrative calculations only; no measured or inferred product efficiency.',
        'area': {'reported_m2_per_g': claimed, 'ideal_two_face_m2_per_g': reference,
                 'corresponding_one_face_m2_per_g': reference / 2,
                 'reported_to_two_face_ratio': round(claimed / reference, 6),
                 'excess_relative_to_two_face_percent': round((claimed / reference - 1) * 100, 6),
                 'reported_to_one_face_ratio': round(claimed / (reference / 2), 6)},
        'thermal': {'assumed_useful_heat_J': round(useful_j, 6),
                    'assumed_useful_heat_Wh': round(useful_wh, 6),
                    'assumed_baseline_task_efficiency': baseline,
                    'scenarios': scenarios, 'power_comparison': powers}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if tracked results differ from recomputation')
    args = parser.parse_args()
    inputs = json.loads((ROOT / 'analysis/model-inputs.json').read_text())
    result = json.dumps(calculate(inputs), ensure_ascii=False, indent=2) + '\n'
    destination = ROOT / 'analysis/results.json'
    if args.check:
        if not destination.exists() or destination.read_text() != result:
            raise SystemExit('FAIL: regenerate analysis/results.json with python tools/analyze.py')
        print('PASS: analytical results reproduce exactly; no product measurements claimed')
    else:
        destination.write_text(result, encoding='utf-8')
        print('Wrote analysis/results.json (illustrative model)')


if __name__ == '__main__':
    main()
