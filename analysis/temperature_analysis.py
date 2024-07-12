#################################################################
#								#
#								#
#		Would a Mighty Smack Tilt Uranus?		#
#								#
#		Louis Eddershaw					#
#								#
#		2023/24						#
#								#
#								#
#################################################################

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
plt.rcParams["mathtext.fontset"] = "cm"


R_earth = 6.371e6

## Read in hdf5 filename
if (len(sys.argv) > 1):
	filepath = sys.argv[1]
else:
	filepath = input("Filepath of the hdf5 file to analyse: ")

## Read in the truncation radius of particles from the origin if requested
if ('-r' in sys.argv):
	max_radius = float(sys.argv[sys.argv.index('-r') + 1])
else:
	max_radius = -1

## Read in the smoothing window width if requested
if ('-w' in sys.argv):
	window_width = int(sys.argv[sys.argv.index('-w') + 1])
else:
	window_width = 25

## Read in whether the plots should be in log scale or not
if ('-log' in sys.argv):
	log_plot = True
else:
	log_plot = False

## Read in the number of particles in the proto-Uranus if requested
if ('-n' in sys.argv):
	target_particles = int(sys.argv[sys.argv.index('-n') + 1])
else:
	target_particles = -1


file_start = 0
for i in range(len(filepath)):
	if filepath[-i] == "/":
		file_start = -i
		break
output_path = "{0}".format(filepath[:file_start])

## Load in EoS tables from WoMa
woma.load_eos_tables()

## Load in particles
pos, vel, h, m, rho, p, u, mat_id, R = custom_woma.load_to_woma(filepath, num_target_particles = target_particles)


## Offset particles such that the centre of mass is situated at the origin
pos_r = np.sqrt(np.sum(pos**2, axis=1)) / R_earth 

com_truncate_mask = np.where(pos_r <= 25)[0]
temp_pos = pos[com_truncate_mask]
temp_m = m[com_truncate_mask]

com = np.sum(temp_m[:, np.newaxis] * temp_pos, axis=0) / (np.sum(temp_m))

pos -= com


## Mask particles that come from the impactor
impactor_indices = mat_id > 400


target_pos = pos[~impactor_indices]
target_vel = vel[~impactor_indices]
target_m = m[~impactor_indices]
target_rho = rho[~impactor_indices]
target_p = p[~impactor_indices]
target_u = u[~impactor_indices]
target_mat_id = mat_id[~impactor_indices]

impactor_pos = pos[impactor_indices]
impactor_vel = vel[impactor_indices]
impactor_m = m[impactor_indices]
impactor_rho = rho[impactor_indices]
impactor_p = p[impactor_indices]
impactor_u = u[impactor_indices]
impactor_mat_id = mat_id[impactor_indices] - 200000000

target_pos_r = np.sqrt(np.sum(target_pos**2, axis=1)) / R_earth
impactor_pos_r = np.sqrt(np.sum(impactor_pos**2, axis=1)) / R_earth

## Mask out particles that are below the maximum truncation radius
if max_radius != -1:
	mask = np.where(target_pos_r < max_radius)[0]
	target_pos_r = target_pos_r[mask]
	target_u = target_u[mask]
	target_rho = target_rho[mask]
	target_mat_id = target_mat_id[mask]

	mask = np.where(impactor_pos_r < max_radius)[0]
	impactor_pos_r = impactor_pos_r[mask]
	impactor_u = impactor_u[mask]
	impactor_rho = impactor_rho[mask]
	impactor_mat_id = impactor_mat_id[mask]


## Compute the temperature of the particles from the particles' internal energy and density, using the relevant EoS
target_temperatures = woma.eos.eos.A1_T_u_rho(target_u, target_rho, target_mat_id) / 10000
impactor_temperatures = woma.eos.eos.A1_T_u_rho(impactor_u, impactor_rho, impactor_mat_id) / 10000

## Sort particles by radial distance from origin
sort = np.argsort(target_pos_r)
target_pos_r = target_pos_r[sort]
target_temperatures = target_temperatures[sort]
target_mat_id = target_mat_id[sort]

sort = np.argsort(impactor_pos_r)
impactor_pos_r = impactor_pos_r[sort]
impactor_temperatures = impactor_temperatures[sort]
impactor_mat_id = impactor_mat_id[sort]


## Smooth temperatures with running average
target_running_average_temperatures = uniform_filter1d(target_temperatures, size=window_width, mode="nearest")
impactor_running_average_temperatures = uniform_filter1d(impactor_temperatures, size=window_width//2, mode="nearest")


impactor_mat_id += 200000000

target_colour = np.empty(len(target_pos_r), dtype=object)
target_sizes = np.ones(len(target_pos_r)) * 13
impactor_colour = np.empty(len(impactor_pos_r), dtype=object)
impactor_sizes = np.ones(len(impactor_pos_r)) * 13

## Colour particles by their material type (including offsetting colours from impactor)
for id_c, c in material_colour_map.ID_COLOUR_MAP.items():
	target_colour[target_mat_id == id_c] = c
	impactor_colour[impactor_mat_id == id_c] = c



reduce_points = 1

## Plot raw temperatures against radial position for both impactor and proto-Uranus

fig = plt.figure(figsize=(7,6))
plt.scatter(target_pos_r[::reduce_points], target_temperatures[::reduce_points], s=18, c=target_colour[::reduce_points], alpha=0.75, linewidth=0)
if log_plot: plt.yscale("log")
plt.xlabel(r"Radius [R$_\oplus$]")
plt.ylabel(r"Temperature [$10^4$ K]")
#plt.xlim(-max_radius*0.05, max_radius)
plt.xlim(2, 3.5)
plt.ylim(-0.5, 10)
plt.tight_layout()
plt.savefig("{0}/target_raw_temperatures.png".format(output_path), dpi=300)
plt.close()

fig = plt.figure(figsize=(7,6))
plt.scatter(impactor_pos_r[::reduce_points], impactor_temperatures[::reduce_points], s=18, c=impactor_colour[::reduce_points], alpha=0.75, linewidth=0)
if log_plot: plt.yscale("log")
plt.xlabel(r"Radius [R$_\oplus$]")
plt.ylabel(r"Temperature [$10^4$ K]")
plt.xlim(-max_radius*0.05, max_radius)
plt.ylim(-0.5, 10)
plt.tight_layout()
plt.savefig("{0}/impactor_raw_temperatures.png".format(output_path), dpi=300)
plt.close()


for id_c, c in material_colour_map.ID_COLOUR_MAP.items():
	target_colour[target_mat_id == id_c] = c
	impactor_colour[impactor_mat_id == id_c] = c

## Plot the smoothed temperatures against radial position for both impactor and proto-Uranus

fig = plt.figure(figsize=(7,6))
plt.scatter(target_pos_r[::reduce_points], target_running_average_temperatures[::reduce_points], s=target_sizes, c=target_colour[::reduce_points], alpha=0.75, linewidth=0)
if log_plot: plt.yscale("log")
plt.xlabel(r"Radius [R$_\oplus$]")
plt.ylabel(r"Averaged Temperature [$10^4$ K]")
plt.xlim(-max_radius*0.05, max_radius)
plt.ylim(-0.5, 10)
plt.tight_layout()
plt.savefig("{0}/target_averaged_temperature.png".format(output_path), dpi=300)
plt.close()

fig = plt.figure(figsize=(7,6))
plt.scatter(impactor_pos_r[::reduce_points], impactor_running_average_temperatures[::reduce_points], s=impactor_sizes, c=impactor_colour[::reduce_points], alpha=0.75, linewidth=0)
if log_plot: plt.yscale("log")
plt.xlabel(r"Radius [R$_\oplus$]")
plt.ylabel(r"Averaged Temperature [$10^4$ K]")
plt.xlim(-max_radius*0.05, max_radius)
plt.ylim(-0.5, 10)
plt.tight_layout()
plt.savefig("{0}/impactor_averaged_temperature.png".format(output_path), dpi=300)
plt.close()


## Do the same again, but this time combine the impactor and proto-Uranus particles together (makes a slight difference to the smoothing process)

combined_pos_r = np.concatenate((target_pos_r, impactor_pos_r))
combined_temperatures = np.concatenate((target_temperatures, impactor_temperatures))
combined_post_running_average_temperatures = np.concatenate((target_running_average_temperatures, impactor_running_average_temperatures))
combined_colour = np.concatenate((target_colour, impactor_colour))
combined_sizes = np.concatenate((target_sizes, impactor_sizes))

fig = plt.figure(figsize=(7,6))
plt.scatter(combined_pos_r[::reduce_points], combined_temperatures[::reduce_points], s=combined_sizes, c=combined_colour[::reduce_points], alpha=0.75, linewidth=0)
if log_plot: plt.yscale("log")
plt.xlabel(r"Radius [R$_\oplus$]")
plt.ylabel(r"Temperature [$10^4$ K]")
plt.xlim(-max_radius*0.05, max_radius)
plt.ylim(-0.5, 10)
plt.tight_layout()
plt.savefig("{0}/combined_raw_temperatures.png".format(output_path), dpi=300)
plt.close()



sort = np.argsort(combined_pos_r)
combined_pre_pos_r = combined_pos_r[sort]
combined_pre_temperatures = combined_temperatures[sort]
combined_pre_colour = combined_colour[sort]
combined_pre_running_average_temperatures = uniform_filter1d(combined_pre_temperatures, size=window_width, mode="nearest")






fig = plt.figure(figsize=(7,6))
plt.scatter(combined_pos_r[::reduce_points], combined_post_running_average_temperatures[::reduce_points], s=18, c=combined_colour[::reduce_points], alpha=0.75, linewidth=0)
if log_plot: plt.yscale("log")
plt.xlabel(r"Radius [R$_\oplus$]")
plt.ylabel(r"Averaged Temperature [$10^4$ K]")
plt.xlim(-max_radius*0.05, max_radius)
plt.tight_layout()
plt.savefig("{0}/combined_post_averaged_temperatures.png".format(output_path), dpi=300)
plt.close()

fig = plt.figure(figsize=(7,6))
plt.scatter(combined_pre_pos_r[::reduce_points], combined_pre_running_average_temperatures[::reduce_points], s=18, c=combined_pre_colour[::reduce_points], alpha=0.75, linewidth=0)
if log_plot: plt.yscale("log")
plt.xlabel(r"Radius [R$_\oplus$]")
plt.ylabel(r"Averaged Temperature [$10^4$ K]")
plt.xlim(-max_radius*0.05, max_radius)
plt.tight_layout()
plt.savefig("{0}/combined_pre_averaged_temperatures.png".format(output_path), dpi=300)
plt.close()




