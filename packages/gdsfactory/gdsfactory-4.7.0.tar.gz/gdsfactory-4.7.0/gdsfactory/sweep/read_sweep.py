"""A Design Of Experiment (DOE) or sweep
changes one or several parameters.
"""

import itertools as it
from io import StringIO
from pathlib import Path
from typing import Any, Dict, List, Union

from omegaconf import OmegaConf

from gdsfactory.config import CONFIG

_sample_yaml_code = """
does:
    cutback_taper_te_400:
      component: cutback_taper_te
      settings:
        wg_width: [0.4]
        length: [1.5]
        n_devices_target: [30, 60, 120]

"""


def read_sweep(filepath: Union[Path, StringIO, str]) -> Dict[str, Any]:
    """Return dictionary with the information loaded from does.yml

    Args:
        filepath: yaml file describing does

    Returns:
        a dictionary of DOEs with:
        {
            doe_name1: [(component_factory_name, parameters), ...]
            doe_name2: [(component_factory_name, parameters), ...]
            ...
        }

    .. code:: yaml

        mmi1x2_gap:
            component: mmi1x2
            gap: [0.5, 0.6]
            length: 10

        mmi1x2:
            component: mmi1x2
            length: [11, 12]
            gap: [0.2, 0.3]
            do_permutation: False

    """
    does = {}
    filepath = (
        StringIO(filepath)
        if isinstance(filepath, str) and "\n" in filepath
        else filepath
    )
    input_does = OmegaConf.load(filepath)
    input_does = OmegaConf.to_container(input_does)

    for doe_name, doe in input_does.items():
        if doe_name == "mask":
            continue
        if doe.get("type", "") == "template":
            continue

        if "do_permutation" in doe:
            do_permutation = doe.pop("do_permutation")
        else:
            do_permutation = True
        if not doe.get("settings"):
            raise ValueError(f"Error, missing settings: for {doe_name!r}")

        doe_settings = doe.pop("settings", "")
        if doe_settings:
            doe["settings"] = get_settings_list(do_permutation, **doe_settings)
        else:
            raise ValueError(
                f"DOE {doe_name!r} is not a dictionary",
                f"\n\t got: {doe!r}\n\t sample: {_sample_yaml_code}",
            )

        does[doe_name] = doe

    return does


def get_settings_list(do_permutations: bool = True, **kwargs) -> List[Dict[str, Any]]:
    """Return a list of settings

    Args:
        do_permutations: if False, will only zip the values passed for each parameter
            True creates all combinations
        kwargs: Keyword arguments with a list or tuple of desired values to sweep

    Usage:

        import gdsfactory as gf

        gf.sweep.read_sweep.get_settings_list(length=[30, 40])  # adds different lengths
        gf.sweep.read_sweep.get_settings_list(length=[30, 40], width=[4, 8])
        gf.sweep.read_sweep.get_settings_list(length=[30, 40], width=[4, 8])
        # if do_permutations=True, does all combinations (L30W4, L30W8, L40W4, L40W8)
        # if do_permutations=False, zips arguments (L30W4, L40W8)


    add variations of self.baseclass in self.components
    get arguments from default_args and then update them from kwargs
    updates default_args with kwargs
    self.settings lists all the variations
    """

    # Deal with empty parameter case
    if kwargs == {}:
        return [dict()]

    # Accept both values or lists
    for key, value in list(kwargs.items()):
        if not isinstance(value, list):
            kwargs[key] = [value]

    if do_permutations:
        keys, list_values = list(zip(*list(kwargs.items())))
        settings = [dict(list(zip(keys, perms))) for perms in it.product(*list_values)]
    else:
        keys, list_values = list(zip(*list(kwargs.items())))
        settings = [dict(list(zip(keys, values))) for values in zip(*list_values)]

    return settings


def test_read_sweep() -> Dict[str, Any]:
    filepath = CONFIG["samples_path"] / "mask" / "does.yml"
    does = read_sweep(filepath)
    assert len(does) == 4
    return does


if __name__ == "__main__":
    test_read_sweep()
    # from pprint import pprint

    # does_path = CONFIG["samples_path"] / "mask" / "does.yml"
    # pprint(load_does(does_path))
