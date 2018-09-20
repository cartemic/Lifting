import json
import pint
import numpy as np


def round_best(weight, _):
    return (np.round((weight - 15) / 10.) * 10 + 15).astype(int)


def round_up(weight, increment):
    return (np.ceil(weight / increment) * increment).astype(int)


def round_down(weight, increment):
    return (np.ceil(weight / increment) * increment).astype(int)


def round_nearest(weight, increment):
    return (np.ceil(weight / increment) * increment).astype(int)


class Program:
    _ureg = pint.UnitRegistry()
    _quant = _ureg.Quantity
    _rounding_funcs = {
        'nearest': round_nearest,
        'up': round_up,
        'down': round_down,
        'best': round_best
    }

    def __init__(
            self,
            squat_max,
            bench_max,
            dead_max,
            units="lb",
            rounding="nearest"
    ):
        self._units = units
        self._maxes = {
            'squat': self._quant(squat_max, units),
            'bench': self._quant(bench_max, units),
            'dead': self._quant(dead_max, units)
        }
        self._round = self._rounding_funcs[rounding]

    def change_max(
            self,
            squat_max=0,
            bench_max=0,
            dead_max=0
    ):
        new_values = {
            'squat': self._quant(squat_max, self._units),
            'bench': self._quant(bench_max, self._units),
            'dead': self._quant(dead_max, self._units)
        }
        self._maxes.update(
            {key: val for key, val in new_values.items() if val.magnitude > 0}
        )

    def change_units(self, new_units):
        if new_units in {'lb', 'kg'}:
            self._maxes = {
                key: value.to(new_units) for key, value in self._maxes.items()
            }
        else:
            raise ValueError('bad units')

    @property
    def squat_max(self):
        return self._maxes['squat']

    @property
    def bench_max(self):
        return self._maxes['bench']

    @property
    def dead_max(self):
        return self._maxes['dead']

    @property
    def _increment(self):
        increments = {
            'lb': 5,
            'kg': 2.5

        }

        return increments[self._units] * 2

    def load(
            self,
            json_path
    ):
        with open(json_path) as f:
            data = json.loads(f.read())
        print(type(data))

        for week_title, week in data.items():
            print(week_title)
            for day_title, day in week.items():
                print('  ', day_title)
                for lift in day:
                    print('    ', lift['name'])
                    lift_max = self._maxes[lift['type'][0]].magnitude
                    for weight, reps in zip(lift['weight'], lift['reps']):
                        weight = self._round(
                            np.array(weight) * lift_max,
                            self._increment
                        )
                        print('        ', weight, 'x', reps)


    # def


if __name__ == "__main__":
    test = Program(435, 285, 485, rounding='best')

    test.load('IML_prep_1.json')
