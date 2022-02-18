"""
Demonstrates using Iris to load data on an unstructured mesh and plot it using
Geovista. Based on Geovista example: https://github.com/bjlittle/geovista/blob/f5c469f4b7afb83bd9e769dffece5ef6c650df32/examples/example_from_unstructured__fesom.py

"""

import geovista as gv
import iris


# see https://fesom.de/cmip6/work-with-awi-cm-unstructured-data/
# https://swift.dkrz.de/v1/dkrz_0262ea1f00e34439850f3f1d71817205/FESOM/tos_Omon_AWI-ESM-1-1-LR_historical_r1i1p1f1_gn_185001-185012.nc
fname = "./tos_Omon_AWI-ESM-1-1-LR_historical_r1i1p1f1_gn_185001-185012.nc"
cube = iris.load_cube(fname, "tos")[0]
lons = cube.coord("longitude").bounds
lats = cube.coord("latitude").bounds

mesh = gv.Transform.from_unstructured(
    lons, lats, lons.shape, data=cube.data, name=cube.name()
)

plotter = gv.GeoPlotter()
sargs = dict(
    fmt="%.1f\u00b0C",
    title="",
    label_font_size=18,
    vertical=True,
    height=0.7,
    position_y=0.15,
)
plotter.add_mesh(
    mesh, cmap="balance", show_edges=True, scalar_bar_args=sargs, edge_color="black"
)
plotter.add_base_layer(color="grey")
plotter.add_axes()
plotter.add_text(
    "Data Source: AWI-ESM CMIP6 FESOM",
    position="lower_right",
    font_size=10,
    shadow=True,
)
plotter.add_title("FESOM Sea Surface Temperature on an Unstructured Mesh", font_size=10)
plotter.camera.position = (3.75, -0.7, 1.86)
plotter.save_graphic("FESOM_Unstructured_tos_data_10.svg")
