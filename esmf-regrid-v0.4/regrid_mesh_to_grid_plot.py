from esmf_regrid.experimental.unstructured_scheme import MeshToGridESMFRegridder
from geovista import GeoPlotter, Transform
from iris import load_cube
from iris.experimental.ugrid import PARSE_UGRID_ON_LOAD
from iris.tests import get_data_path
import numpy as np

# Load cubes.
mesh_file = get_data_path(
    ["NetCDF", "unstructured_grid", "lfric_surface_mean.nc"]
)
grid_file = get_data_path(
    ["NetCDF", "regrid", "regrid_template_global_latlon.nc"]
)

with PARSE_UGRID_ON_LOAD.context():
    mesh_cube = load_cube(mesh_file, "sea_surface_temperature")

# Create a demonstration aberration.
np.put(mesh_cube.data, [2304, 2305, 2352, 2353], 300)

# Regrid.
sample_grid = load_cube(grid_file)
rg = MeshToGridESMFRegridder(mesh_cube, sample_grid)
grid_cube = rg(mesh_cube)

###############################################################################

# Create PolyDatas.
mesh_lons, mesh_lats = mesh_cube.mesh.node_coords
face_node = mesh_cube.mesh.face_node_connectivity
indices = face_node.indices_by_location()
mesh_polydata = Transform.from_unstructured(
    mesh_lons.points,
    mesh_lats.points,
    indices,
    data=mesh_cube.data,
    name="modelled_temperature / K",
    start_index=face_node.start_index,
)

grid_lons = grid_cube.coord("longitude")
grid_lats = grid_cube.coord("latitude")
grid_polydata = Transform.from_1d(grid_lons.points,
                         grid_lats.points,
                         data=grid_cube.data,
                         name="modelled_temperature / K",
                         )

# Create plotter.
my_plotter = GeoPlotter(shape=(1, 2))
my_plotter.camera.zoom(0.75)


def plot_polydata(polydata, text):
    my_plotter.add_text(text, font_size=12)
    my_plotter.add_coastlines("50m")
    my_plotter.add_mesh(polydata, show_edges=True)


# Plot PolyDatas.
my_plotter.subplot(0, 0)
plot_polydata(mesh_polydata, "Original")

my_plotter.subplot(0, 1)
my_plotter.link_views()
plot_polydata(grid_polydata, "Regridded")

my_plotter.show(screenshot="iris-esmf-regrid-demo.png")
