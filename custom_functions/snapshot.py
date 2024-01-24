import swiftsimio as sw
import unyt
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from custom_functions import material_colour_map

def get_pos_mat_id(snapshot_path, ax_lim, num_target_particles, mask_window_length=-1):
	""" Select and load the particles to plot. """

	# Only load data with the axis limits (if provided) and below z=0
	mask = sw.mask(snapshot_path)
	
	box_length = mask.metadata.boxsize[0].to(unyt.Rearth)
	box_mid = box_length / 2
	if ax_lim == -1: ax_lim = 1.5 * float(box_mid)

	if mask_window_length == -1:
		mask_min = box_mid - ax_lim * unyt.Rearth
		mask_max = box_mid + ax_lim * unyt.Rearth
	else:
		mask_min = box_mid - mask_window_length * unyt.Rearth
		mask_max = box_mid + mask_window_length * unyt.Rearth

	load_region = [[mask_min, mask_max], [mask_min, mask_max], [mask_min, box_mid]]
	mask.constrain_spatial(load_region)

	# Load
	data = sw.load(snapshot_path, mask=mask)
	pos = data.gas.coordinates.to(unyt.Rearth) - box_mid
	id = data.gas.particle_ids
	mat_id = data.gas.material_ids.value

	# Restrict to z < 0
	sel = np.where(pos[:, 2] < 0)[0]
	pos = pos[sel]
	id = id[sel]
	mat_id = mat_id[sel]

	# Sort in z order so higher particles are plotted on top
	sort = np.argsort(pos[:, 2])
	pos = pos[sort]
	id = id[sort]
	mat_id = mat_id[sort]

	if num_target_particles != -1:
		# Edit material IDs for particles in the impactor
		mat_id[num_target_particles <= id] += material_colour_map.id_body

	return pos, mat_id, ax_lim


def plot_pos_mat_id(pos, mat_id, ax_lim, simulation_name, snapshot_id, time_step="undefined", final_output=False, x_axes="undefined", y_axes="undefined"):
	""" Plot the particles, coloured by their material. """
	plt.figure(figsize=(7, 7))
	ax = plt.gca()
	ax.set_aspect("equal")

	colour = np.empty(len(pos), dtype=object)
	for id_c, c in material_colour_map.ID_COLOUR_MAP.items():
		colour[mat_id == id_c] = c

	ax.scatter(
		pos[:, 0], pos[:, 1], c=colour, edgecolors="none", marker=".", s=10, alpha=0.5
	)


	if final_output:
		font_size = 60
	else:
		font_size = matplotlib.rcParams['font.size']

	ax.set_xlim(-ax_lim, ax_lim)
	ax.set_ylim(-ax_lim, ax_lim)
	ax.set_yticks(ax.get_xticks())

	ax.set_xlabel(r"x Position ($R_\oplus$)")
	
	ax.xaxis.label.set_fontsize(font_size/2)
	for label in (ax.get_xticklabels()):
		label.set_fontsize(font_size/3)


	if x_axes != True:
		ax.xaxis.label.set_color('black')
		ax.tick_params(axis='x', colors='black')

	ax.set_ylabel(r"y Position ($R_\oplus$)")

	ax.yaxis.label.set_fontsize(font_size/2)
	for label in (ax.get_yticklabels()):
		label.set_fontsize(font_size/3)


	if y_axes != True:
		ax.yaxis.label.set_color('black')
		ax.tick_params(axis='y', colors='black')

	if time_step != "undefined":
		hours = int(abs(time_step) // 3600)
		and_minutes = int((abs(time_step) - (hours * 3600)) // 60)
		time_text = "{0}h {1}m".format(hours, and_minutes)
		if time_step > 0:
			time_text = "+{0}".format(time_text)
		elif time_step < 0:
			time_text = "-{0}".format(time_text)

		time_text = "{0}".format(time_text)
		
	else:
		time_text = ""


	title_text = ""

	if not final_output:
		title_text = "{0}\nSnapshot {1}\n".format(simulation_name, snapshot_id)

	title_text = "{0}{1}".format(title_text, time_text)
	plt.title(title_text, fontsize=font_size)

	plt.tight_layout()