import sys
import yaml
import json
from typing import Any


def load_dispatch_inputs(filepath) -> Any:
    with open(filepath, 'r') as stream:
        dict = yaml.load(stream, Loader=yaml.BaseLoader)
    return dict['on']['workflow_dispatch']['inputs']


def load_actual_inputs(filepath) -> Any:
    with open(filepath, 'r') as stream:
        json_file = json.load(stream)
    str = json_file['body']
    i = str.find('\ninputs:')
    if i >= 0:
        dict = yaml.load(str[i:], Loader=yaml.BaseLoader)
        return dict['inputs']
    return {}


def _main():
    if len(sys.argv) != 3:
        raise ValueError('Expected 2 arguments')

    # Load dispatch inputs
    dispatch_inputs = load_dispatch_inputs(sys.argv[1])

    # Load actual inputs
    actual_inputs = load_actual_inputs(sys.argv[2])

    # Resolve the inputs
    resolved_inputs = {}
    for key, val in dispatch_inputs.items():
        if key in actual_inputs:
            resolved_inputs[key] = actual_inputs[key]
        elif 'default' in val:
            resolved_inputs[key] = val['default']
        else:
            resolved_inputs[key] = ''

    # Output JSON
    str = json.dumps(resolved_inputs, indent=2)
    print(str)


if __name__ == "__main__":
    _main()
