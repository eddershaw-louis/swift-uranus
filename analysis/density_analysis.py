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

import csv

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


## Read in name of hdf5 file
if (len(sys.argv) > 1):
	filepath = sys.argv[1]
else:
	filepath = input("Filepath of the hdf5 file to analyse: ")

## Read in density floor if requested
if ('-df' in sys.argv):
	density_floor = float(sys.argv[sys.argv.index('-df') + 1])
else:
	density_floor = -1

## Read in the truncation radius of particles from the origin if requested
if ('-r' in sys.argv):
	max_radius = float(sys.argv[sys.argv.index('-r') + 1])
else:
	max_radius = -1

## Read in the smoothing window width if requested
if ('-w' in sys.argv):
	window_width = int(sys.argv[sys.argv.index('-w') + 1])
else:
	window_width = 13

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

## Read in the pre-impact rotation vector of the proto-Uranus if requested
if ('-ref' in sys.argv):
	reference_filepath = sys.argv[sys.argv.index('-ref') + 1]
	reference = True
else:
	reference = False

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
impactor_mat_id = mat_id[impactor_indices] #- 200000000


target_pos_r = np.sqrt(np.sum(target_pos**2, axis=1)) / R_earth
impactor_pos_r = np.sqrt(np.sum(impactor_pos**2, axis=1)) / R_earth

## Mask out particles that are above the density floor
if density_floor > 0:
	sort = np.argsort(target_pos_r)
	target_pos_r = target_pos_r[sort]
	target_rho = target_rho[sort]
	target_mat_id = target_mat_id[sort]

	sort = np.argsort(impactor_pos_r)
	impactor_pos_r = impactor_pos_r[sort]
	impactor_rho = impactor_rho[sort]
	impactor_mat_id = impactor_mat_id[sort]


	temp_truncate_mask = np.where(target_pos_r <= 25)[0]
	target_temp_rho = target_rho[temp_truncate_mask]

	temp_truncate_mask = np.where(impactor_pos_r <= 25)[0]
	impactor_temp_rho = impactor_rho[temp_truncate_mask]


	target_running_average_rho = uniform_filter1d(target_temp_rho, size=window_width // 2, mode="nearest")
	impactor_running_average_rho = uniform_filter1d(impactor_temp_rho, size=window_width // 4, mode="nearest")

	target_mask = np.where(target_running_average_rho >= density_floor)[0]
	impactor_mask = np.where(impactor_running_average_rho >= density_floor)[0]


## Mask out particles that are below the maximum truncation radius
elif max_radius > 0:
	target_mask = np.where(target_pos_r <= max_radius)[0]
	impactor_mask = np.where(impactor_pos_r <= max_radius)[0]
	print("Clipping max radius")

## Do the masking as deduced previously
if density_floor > 0 or max_radius > 0: 
	target_pos_r = target_pos_r[target_mask]
	target_rho = target_rho[target_mask]
	target_mat_id = target_mat_id[target_mask]

	impactor_pos_r = impactor_pos_r[impactor_mask]
	impactor_rho = impactor_rho[impactor_mask]
	impactor_mat_id = impactor_mat_id[impactor_mask]


## Sort particles by radial distance from origin
sort = np.argsort(target_pos_r)
target_pos_r = target_pos_r[sort]
target_rho = target_rho[sort]
target_mat_id = target_mat_id[sort]

sort = np.argsort(impactor_pos_r)
impactor_pos_r = impactor_pos_r[sort]
impactor_rho = impactor_rho[sort]
impactor_mat_id = impactor_mat_id[sort]



target_colour = np.empty(len(target_pos_r), dtype=object)
target_sizes = np.ones(len(target_pos_r)) * 13

impactor_colour =np.empty(len(impactor_pos_r), dtype=object)
impactor_sizes = np.ones(len(impactor_pos_r)) * 13

## Colour particles by their material type (including offsetting colours from impactor)
for id_c, c in material_colour_map.ID_COLOUR_MAP.items():
	target_colour[target_mat_id == id_c] = c
	impactor_colour[impactor_mat_id == id_c] = c
	



## Plot raw densities against radial position for both impactor and proto-Uranus

fig = plt.figure(figsize=(7,6))
plt.scatter(target_pos_r, target_rho, s=target_sizes, c=target_colour, alpha=0.25, linewidth=0)

if max_radius > 0:
	plt.xlim(plt.gca().get_xlim()[0], max_radius)
if log_plot: plt.yscale("log")
plt.xlabel(r"Radius [R$_\oplus$]")
plt.ylabel(r"Density [kg m$^{-3}$]")
plt.xlim(-max_radius*0.05, max_radius)
plt.tight_layout()
plt.savefig("{0}/target_raw_density.png".format(output_path), dpi=300)
plt.close()

#with open("{0}_raw_target_densities.txt".format(filepath[:-5]), "w") as writer:
#	writer.write("{0}\n".format(list(target_pos_r)))
#	writer.write("{0}\n".format(list(target_rho)))

#quit()

fig = plt.figure(figsize=(7,6))
plt.scatter(impactor_pos_r, impactor_rho, s=impactor_sizes, c=impactor_colour, alpha=0.25, linewidth=0)

if max_radius > 0:
	plt.xlim(plt.gca().get_xlim()[0], max_radius)
if log_plot: plt.yscale("log")
plt.xlabel(r"Radius [R$_\oplus$]")
plt.ylabel(r"Density [kg m$^{-3}$]")
plt.xlim(-max_radius*0.05, max_radius)
plt.tight_layout()
plt.savefig("{0}/impactor_raw_density.png".format(output_path), dpi=300)
plt.close()


## Smooth densities with running average
target_running_average_rho = uniform_filter1d(target_rho, size=window_width, mode="nearest")
impactor_running_average_rho = uniform_filter1d(impactor_rho, size=window_width//2, mode="nearest")

## Deduce the radial distance where the averaged density drops below the density floor 
if density_floor > 0:
	mask = np.where(target_running_average_rho >= density_floor)[0]
	target_pos_r_truncated = target_pos_r[mask]
	print("Target, density floor of {0} g/cm^3 reached at: {1} R_earth".format(density_floor, target_pos_r_truncated[-1]))
	
	mask = np.where(impactor_running_average_rho >= density_floor)[0]
	impactor_pos_r_truncated = impactor_pos_r[mask]
	print("Impactor, density floor of {0} g/cm^3 reached at: {1} R_earth".format(density_floor, impactor_pos_r_truncated[-1]))

	## Save findings to file
	with open("{0}_density_analysis.txt".format(filepath[:-5]), "w") as writer:
		writer.write("{0}\n\n".format(str(sys.argv)))
		writer.write("Target, density floor of {0} g/cm^3 reached at {1} R_earth\n".format(density_floor, target_pos_r_truncated[-1]))
		writer.write("Impactor, density floor of {0} g/cm^3 reached at {1} R_earth".format(density_floor, impactor_pos_r_truncated[-1]))


## Plot the smoothed densities against radial position for both impactor and proto-Uranus

fig = plt.figure(figsize=(7,6))
plt.scatter(target_pos_r, target_running_average_rho, s=target_sizes, c=target_colour, alpha=0.25, linewidth=0)

if max_radius > 0:
	plt.xlim(plt.gca().get_xlim()[0], max_radius)

if log_plot: plt.yscale("log")

plt.xlabel(r"Radius [R$_\oplus$]")
#plt.ylabel(r"Averaged Density [kg m$^{-3}$]")
plt.ylabel(r"Density [kg m$^{-3}$]")
plt.xlim(-max_radius*0.05, max_radius)
plt.tight_layout()
plt.savefig("{0}/target_averaged_density.png".format(output_path), dpi=300)
plt.close()


fig = plt.figure(figsize=(7,6))
plt.scatter(impactor_pos_r, impactor_running_average_rho, s=impactor_sizes, c=impactor_colour, alpha=0.25, linewidth=0)

if max_radius > 0:
	plt.xlim(plt.gca().get_xlim()[0], max_radius)

if log_plot: plt.yscale("log")

plt.xlabel(r"Radius [R$_\oplus$]")
#plt.ylabel(r"Averaged Density [kg m$^{-3}$]")
plt.ylabel(r"Density [kg m$^{-3}$]")
plt.xlim(-max_radius*0.05, max_radius)
plt.tight_layout()
plt.savefig("{0}/impactor_averaged_density.png".format(output_path), dpi=300)
plt.close()



## Do the same again, but this time combine the impactor and proto-Uranus particles together (makes a slight difference to the smoothing process)

combined_pos_r = np.concatenate((target_pos_r, impactor_pos_r))
combined_rho = np.concatenate((target_rho, impactor_rho))
combined_post_running_average_rho = np.concatenate((target_running_average_rho, impactor_running_average_rho))
combined_colour = np.concatenate((target_colour, impactor_colour))
combined_sizes = np.concatenate((target_sizes, impactor_sizes))

reduce_points = 1


fig = plt.figure(figsize=(7,6))
plt.scatter(combined_pos_r[::reduce_points], combined_rho[::reduce_points], s=combined_sizes[::reduce_points], c=combined_colour[::reduce_points], alpha=0.25, linewidth=0)
if reference:
	with open("{0}".format(reference_filepath), 'r') as reference_file:
		contents = csv.reader(reference_file, delimiter=',')
		reference_data = [np.asarray(row, dtype=float) for row in contents]
	
	plt.plot(reference_data[0], reference_data[1], c="black")

if log_plot: plt.yscale("log")
plt.xlabel(r"Radius [R$_\oplus$]")
plt.ylabel(r"Density [kg m$^{-3}$]")
plt.xlim(-max_radius*0.05, max_radius)
#plt.ylim(-0.5, 10)
plt.tight_layout()
plt.savefig("{0}/combined_raw_density.png".format(output_path), dpi=300)
plt.close()




sort = np.argsort(combined_pos_r)
combined_pre_pos_r = combined_pos_r[sort]
combined_pre_rho = combined_rho[sort]
combined_pre_colour = combined_colour[sort]
combined_pre_running_average_rho = uniform_filter1d(combined_pre_rho, size=window_width, mode="nearest")






fig = plt.figure(figsize=(7,6))
plt.scatter(combined_pos_r[::reduce_points], combined_post_running_average_rho[::reduce_points], s=combined_sizes[::reduce_points], c=combined_colour[::reduce_points], alpha=0.25, linewidth=0)
if log_plot: plt.yscale("log")
plt.xlabel(r"Radius [R$_\oplus$]")
plt.ylabel(r"Density [kg m$^{-3}$]")
plt.xlim(-max_radius*0.05, max_radius)
#plt.ylim(-0.5, 10)
plt.tight_layout()
plt.savefig("{0}/combined_post_averaged_density.png".format(output_path), dpi=300)
plt.close()

fig = plt.figure(figsize=(7,6))
plt.scatter(combined_pre_pos_r[::reduce_points], combined_pre_running_average_rho[::reduce_points], s=combined_sizes[::reduce_points], c=combined_pre_colour[::reduce_points], alpha=0.25, linewidth=0)
if log_plot: plt.yscale("log")
plt.xlabel(r"Radius [R$_\oplus$]")
plt.ylabel(r"Density [kg m$^{-3}$]")
plt.xlim(-max_radius*0.05, max_radius)
#plt.ylim(-0.5, 10)
plt.tight_layout()
plt.savefig("{0}/combined_pre_averaged_density.png".format(output_path), dpi=300)
plt.close()
