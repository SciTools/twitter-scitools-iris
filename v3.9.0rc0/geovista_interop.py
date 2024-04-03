import requests
from tempfile import NamedTemporaryFile

from geovista import GeoPlotter
import iris
from iris.experimental.geovista import cube_to_polydata
from iris.experimental.ugrid import PARSE_UGRID_ON_LOAD

surface_mean_url = "https://github.com/SciTools/iris-test-data/raw/master/test_data/NetCDF/unstructured_grid/lfric_surface_mean.nc"
response = requests.get(surface_mean_url)
surface_mean_file = NamedTemporaryFile()
surface_mean_file.write(response.content)

with PARSE_UGRID_ON_LOAD.context():
    rainfall_flux_cube = iris.load_cube(surface_mean_file.name, "rainfall_flux")

rainfall_flux_polydata = cube_to_polydata(rainfall_flux_cube[0])
plotter = GeoPlotter(off_screen=True)
plotter.add_mesh(rainfall_flux_polydata, show_edges=True, edge_color="grey")
plotter.add_coastlines()
plotter.add_title("New `cube_to_polydata()` function!")
plotter.screenshot("geovista_interop.png")
