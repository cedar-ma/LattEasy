import os
from pathlib import Path
import shutil
from latteasy.preprocessing.foam_tools import FoamSimulation

here = Path(__file__).resolve().parent
os.chdir(here)

geometry_file = here/"input/gumbo_fracture_3Dhorrizontal_1280_550_50.dat"
domain_size = (1280, 550, 50)
num_cores = 2



# Cold start only: FoamSimulation always invokes `foam_flow <xml>` with no
# second argument, so foam_flow.cpp takes the nucleateBubbles() branch and
# starts at iT = 0. Overrides below match examples/foam_flow/rough_restart.xml;
# leave params={} to just use FoamSimulation.DEFAULT_PARAMS as-is.

simulation = FoamSimulation(
    geometry_file, domain_size, cpus=num_cores, mpi_launcher="ibrun",
    params={"Nucleation": {"distribution": "list", "numberOfBubbles": 300, "radius": 12, "shift": 20, "packingOffset": 3},
    "output": {"outIter": 500, "save_it": 10000},
    },  
)
for ax in "xyz":
    shutil.copy(f"nucleation_{ax}_points.txt", simulation.out_path)

history_log = simulation.run_sim()

print(f"Cores: {num_cores}")
print(f"Nuclei placed: {len(simulation.nuclei)}")
print(f"Bubble history log: {Path(history_log).resolve()}")
print(f"Simulation folder: {Path(simulation.folder_path).resolve()}")
