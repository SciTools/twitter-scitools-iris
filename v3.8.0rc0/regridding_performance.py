from pathlib import Path
from time import time

import matplotlib.pyplot as plt
import numpy as np

from iris.analysis import AreaWeightedRegridder as AreaWeightedRegridder
from iris.cube import Cube
from iris.coords import DimCoord

from _area_weighted_old import AreaWeightedRegridder as AreaWeightedRegridderOld


def gen_cubes(src_size, tgt_size):
    h = 10

    bounds = np.linspace(-90, 90, src_size + 1)
    bounds = np.stack([bounds[:-1], bounds[1:]], axis=1)
    src_lat = DimCoord(np.linspace(-90, 90, src_size), bounds=bounds,
                       standard_name="latitude", units="degrees")
    src_lon = DimCoord(np.linspace(-180, 180, src_size), bounds=bounds * 2,
                       standard_name="longitude", units="degrees")
    src = Cube(np.ones([h, src_size, src_size]))
    src.add_dim_coord(src_lat, 1)
    src.add_dim_coord(src_lon, 2)

    tgt_bounds = np.linspace(-90, 90, tgt_size + 1)
    tgt_bounds = np.stack([tgt_bounds[:-1], tgt_bounds[1:]], axis=1)
    tgt_lat = DimCoord(np.linspace(-90, 90, tgt_size), bounds=tgt_bounds,
                       standard_name="latitude", units="degrees")
    tgt_lon = DimCoord(np.linspace(-180, 180, tgt_size), bounds=tgt_bounds * 2,
                       standard_name="longitude", units="degrees")
    tgt = Cube(np.ones([tgt_size, tgt_size]))
    tgt.add_dim_coord(tgt_lat, 0)
    tgt.add_dim_coord(tgt_lon, 1)
    return src, tgt


src, tgt = gen_cubes(1000, 800)

old_times = []
new_times = []

for size in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
    src, tgt = gen_cubes(size, size - 1)
    t = time()
    rg = AreaWeightedRegridderOld(src, tgt)
    result = rg(src)
    old_times.append(time() - t)

    t = time()
    rg = AreaWeightedRegridder(src, tgt)
    result = rg(src)
    new_times.append(time() - t)

    print(f"{size} done")


plt.plot([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000], old_times, label="old method")
plt.plot([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000], new_times, label="new method")
plt.legend()
plt.title("Regridding performance")
plt.gca().set_xlabel("grid size")
plt.gca().set_ylabel("time (s)")
plt.savefig(Path(__file__).with_suffix(".png"))
