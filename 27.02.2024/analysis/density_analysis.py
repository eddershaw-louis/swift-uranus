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

if ('-df' in sys.argv):
	density_floor = float(sys.argv[sys.argv.index('-df') + 1])
else:
	density_floor = -1

if ('-r' in sys.argv):
	max_radius = float(sys.argv[sys.argv.index('-r') + 1])
else:
	max_radius = -1

if ('-w' in sys.argv):
	window_width = int(sys.argv[sys.argv.index('-w') + 1])
else:
	window_width = 13


file_start = 0
for i in range(len(filepath)):
	if filepath[-i] == "/":
		file_start = -i
		break
output_path = "{0}".format(filepath[:file_start])

woma.load_eos_tables()

pos, vel, h, m, rho, p, u, mat_id, R = custom_woma.load_to_woma(filepath)



pos_r = np.sqrt(np.sum(pos**2, axis=1)) / R_earth 

com_truncate_mask = np.where(pos_r <= 25)[0]
temp_pos = pos[com_truncate_mask]
temp_m = m[com_truncate_mask]

com = np.sum(temp_m[:, np.newaxis] * temp_pos, axis=0) / (np.sum(temp_m))

pos -= com

pos_r = np.sqrt(np.sum(pos**2, axis=1)) / R_earth


if density_floor > 0:
	sort = np.argsort(pos_r)
	pos_r = pos_r[sort]
	rho = rho[sort]

	temp_truncate_mask = np.where(pos_r <= 25)[0]
	temp_rho = rho[temp_truncate_mask]

	running_average_rho = uniform_filter1d(temp_rho, size=window_width // 2, mode="nearest")

	mask = np.where(running_average_rho > density_floor)[0]
elif max_radius > 0:
	mask = np.where(pos_r <= max_radius)[0]
	print("Clipping max radius")

if density_floor > 0 or max_radius > 0: 
	pos_r = pos_r[mask]
	rho = rho[mask]



sort = np.argsort(pos_r)
pos_r = pos_r[sort]
rho = rho[sort]

fig = plt.figure(figsize=(7,7))
plt.plot(pos_r, rho)

if max_radius > 0:
	plt.xlim(plt.gca().get_xlim()[0], max_radius)
#plt.yscale("log")
plt.xlabel(r"Radial Position [R$_\odot$]")
plt.ylabel(r"Density [g cm$^{-3}$]")
plt.tight_layout()
plt.savefig("{0}/raw_density.png".format(output_path))
plt.close()

running_average_rho = uniform_filter1d(rho, size=window_width, mode="nearest")

if density_floor > 0:
	mask = np.where(running_average_rho >= density_floor)[0]
	pos_r_truncated = pos_r[mask]
	print("Density floor of {0} g/cm^3 reached at: {1} R_earth".format(density_floor, pos_r_truncated[-1]))
	
	with open("{0}_density_analysis.txt".format(filepath[:-5]), "w") as writer:
		writer.write("{0}\n\n".format(str(sys.argv)))
		writer.write("Density floor of {0} g/cm^3 reached at {1} R_earth".format(density_floor, pos_r_truncated[-1]))

fig = plt.figure(figsize=(7,7))
plt.plot(pos_r, running_average_rho)

if max_radius > 0:
	plt.xlim(plt.gca().get_xlim()[0], max_radius)

#plt.yscale("log")
plt.xlabel(r"Radial Position [R$_\odot$]")
plt.ylabel(r"Averaged Density [g cm$^{-3}$]")
plt.tight_layout()
plt.savefig("{0}/averaged_density.png".format(output_path))
plt.close()


