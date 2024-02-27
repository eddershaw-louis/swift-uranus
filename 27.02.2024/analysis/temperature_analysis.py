import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import swiftsimio as sw
import unyt

import sys
import math
import numpy as np
from scipy.ndimage import uniform_filter1d

import woma

sys.path.append("..")
sys.path.append("../..")

from custom_functions import snapshot
from custom_functions import material_colour_map
from custom_functions import custom_woma

font_size = 20
params = {
    "axes.labelsize": font_size,
    "font.size": font_size,
    "xtick.labelsize": font_size,
    "ytick.labelsize": font_size,
    "font.family": "serif",
}
matplotlib.rcParams.update(params)

R_earth = 6.371e6


if (len(sys.argv) > 1):
	filepath = sys.argv[1]
else:
	filepath = input("Filepath of the hdf5 file to analyse: ")


if ('-r' in sys.argv):
	max_radius = float(sys.argv[sys.argv.index('-r') + 1])
else:
	max_radius = -1

if ('-w' in sys.argv):
	window_width = int(sys.argv[sys.argv.index('-w') + 1])
else:
	window_width = 25


file_start = 0
for i in range(len(filepath)):
	if filepath[-i] == "/":
		file_start = -i
		break
output_path = "{0}".format(filepath[:file_start])

woma.load_eos_tables()

pos, vel, h, m, rho, p, u, mat_id, R = custom_woma.load_to_woma(filepath)
pos_r = np.sqrt(np.sum(pos**2, axis=1)) / R_earth

if max_radius != -1:
	mask = np.where(pos_r < max_radius)[0]
	pos_r = pos_r[mask]
	u = u[mask]
	rho = rho[mask]
	mat_id = mat_id[mask]

temperatures = woma.eos.eos.A1_T_u_rho(u, rho, mat_id)

sort = np.argsort(pos_r)
pos_r = pos_r[sort]
temperatures = temperatures[sort]


running_average_temperatures = uniform_filter1d(temperatures, size=window_width, mode="nearest")



fig = plt.figure(figsize=(7,7))
plt.plot(pos_r, temperatures)
#plt.yscale("log")
plt.xlabel(r"Radial Position [R$_\odot$]")
plt.ylabel("Temperature [K]")
raw_y_lim = plt.gca().get_ylim()
plt.tight_layout()
plt.savefig("{0}/raw_temperatures.png".format(output_path))
plt.close()


fig = plt.figure(figsize=(7,7))
plt.plot(pos_r, running_average_temperatures)
#plt.yscale("log")
plt.xlabel(r"Radial Position [R$_\odot$]")
plt.ylabel("Averaged Temperature [K]")
#plt.ylim(raw_y_lim[0], raw_y_lim[1])
plt.tight_layout()
plt.savefig("{0}/averaged_temperature.png".format(output_path))
plt.close()
