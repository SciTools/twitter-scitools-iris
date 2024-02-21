from pathlib import Path

from cartopy.io import shapereader
from matplotlib import pyplot as plt

import iris
import iris.quickplot as qplt
from iris.util import mask_cube_from_shapefile


hires_path = Path(
    "~myeo",
    "repos",
    "iris-test-data",
    "test_data",
    "NetCDF",
    "global",
    "xyt",
    "SMALL_hires_wind_u_for_ipcc4.nc"
).expanduser()
my_cube = iris.load_cube(hires_path)

ne_countries = shapereader.natural_earth(
    resolution="10m", category="cultural", name="admin_0_countries"
)
reader = shapereader.Reader(ne_countries)
russia = [
    country.geometry
    for country in reader.records()
    if "Russia" in country.attributes["NAME_LONG"]
][0]

masked_cube_russia_weighted = mask_cube_from_shapefile(
    my_cube,
    russia,
    minimum_weight=0.99
)

qplt.pcolormesh(masked_cube_russia_weighted[0])
plt.gca().coastlines()
plt.gca().set_title("Masked to Russia's shape")
plt.savefig(Path(__file__).with_suffix(".png"))
