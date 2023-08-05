import itertools as it
from typing import Any, Dict, List

from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.grid import grid, grid_with_text
from gdsfactory.pack import pack
from gdsfactory.types import ComponentFactory, Optional


@cell
def pack_doe(
    component_factory: ComponentFactory,
    settings: Dict[str, List[Any]],
    do_permutations: bool = False,
    function: Optional[ComponentFactory] = None,
    **kwargs,
) -> Component:
    """Packs a component DOE (Design of Experiment) using pack.

    Args:
        component_factory: function to return Components.
        settings: component_factory settings.
        do_permutations: for each setting.
        function: for the component (add padding, grating couplers ...)

    keyword Args:
        component_factory: list or tuple
        spacing: Minimum distance between adjacent shapes
        aspect_ratio: (width, height) ratio of the rectangular bin
        max_size: Limits the size into which the shapes will be packed
        sort_by_area: Pre-sorts the shapes by area
        density: Values closer to 1 pack tighter but require more computation
        precision: Desired precision for rounding vertex coordinates.
        text: Optional function to add text labels.
        text_prefix: for labels. For example. 'A' will produce 'A1', 'A2', ...
        text_offsets: relative to component size info anchor. Defaults to center.
        text_anchors: relative to component (ce cw nc ne nw sc se sw center cc).
        name_prefix: for each packed component (avoids the Unnamed cells warning).
            Note that the suffix contains a uuid so the name will not be deterministic
        rotation: for each component in degrees
        h_mirror: horizontal mirror in y axis (x, 1) (1, 0). This is the most common.
        v_mirror: vertical mirror using x axis (1, y) (0, y)
    """
    if do_permutations:
        settings_list = [dict(zip(settings, t)) for t in it.product(*settings.values())]
    else:
        settings_list = [dict(zip(settings, t)) for t in zip(*settings.values())]

    if function:
        component_list = [
            function(component_factory(**settings)) for settings in settings_list
        ]
    else:
        component_list = [component_factory(**settings) for settings in settings_list]

    c = pack(component_list=component_list, **kwargs)
    if len(c) > 1:
        raise ValueError(
            f"failed to pack in one Component, it created {len(c)} Components"
        )
    else:
        return c[0]


@cell
def pack_doe_grid(
    component_factory: ComponentFactory,
    settings: Dict[str, List[Any]],
    do_permutations: bool = False,
    function: Optional[ComponentFactory] = None,
    with_text: bool = False,
    **kwargs,
) -> Component:
    """Packs a component DOE (Design of Experiment) using grid.

    Args:
        component_factory: function to return Components.
        settings: component_factory settings.
        do_permutations: for each setting.
        function: for the component (add padding, grating couplers ...)
        with_text: includes text label.

    keyword Args:
        spacing: between adjacent elements on the grid, can be a tuple for
            different distances in height and width.
        separation: If True, guarantees elements are speparated with fixed spacing
            if False, elements are spaced evenly along a grid.
        shape: x, y shape of the grid (see np.reshape).
            If no shape and the list is 1D, if np.reshape were run with (1, -1).
        align_x: {'x', 'xmin', 'xmax'} for x (column) alignment along
        align_y: {'y', 'ymin', 'ymax'} for y (row) alignment along
        edge_x: {'x', 'xmin', 'xmax'} for x (column) (ignored if separation = True)
        edge_y: {'y', 'ymin', 'ymax'} for y (row) (ignored if separation = True)
        rotation: for each component in degrees.
        h_mirror: horizontal mirror y axis (x, 1) (1, 0). most common mirror.
        v_mirror: vertical mirror using x axis (1, y) (0, y).
    """
    if do_permutations:
        settings_list = [dict(zip(settings, t)) for t in it.product(*settings.values())]
    else:
        settings_list = [dict(zip(settings, t)) for t in zip(*settings.values())]

    if function:
        component_list = [
            function(component_factory(**settings)) for settings in settings_list
        ]
    else:
        component_list = [component_factory(**settings) for settings in settings_list]

    if with_text:
        return grid_with_text(component_list, **kwargs)

    else:
        return grid(component_list, **kwargs)


if __name__ == "__main__":
    import gdsfactory as gf

    c = pack_doe_grid(
        component_factory=gf.c.mmi1x2,
        settings=dict(length_mmi=[2, 100], width_mmi=[4, 10]),
        with_text=True,
        spacing=(100, 100),
        shape=(2, 2),
        # settings=dict(length_mmi=[2, 100], width_mmi=[4, 10]),
        do_permutations=True,
    )
    c.show()
    # settings = dict(length_mmi=[2, 100], width_mmi=[4, 10])
    # settings_list = [dict(zip(settings, t)) for t in zip(*settings.values())]
