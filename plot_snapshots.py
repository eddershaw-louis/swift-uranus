###############################################################################
# This file is part of SWIFT.
# Copyright (c) 2019 Jacob Kegerreis (jacob.kegerreis@durham.ac.uk)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# Plot the snapshots from the example giant impact on the proto-Earth, showing
# the particles in a thin slice near z=0, coloured by their material.

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import swiftsimio as sw
import unyt

import glob
import sys
import os
import math

from custom_functions import material_colour_map
from custom_functions import snapshot

font_size = 20
params = {
    "axes.labelsize": font_size,
    "font.size": font_size,
    "xtick.labelsize": font_size,
    "ytick.labelsize": font_size,
    "font.family": "serif",
}
plt.style.use('dark_background')
matplotlib.rcParams.update(params)




if (len(sys.argv) > 1):
	simulation_name = sys.argv[1]
else:
	simulation_name = input("Enter the name of the simulation: ")

assumed_ax_lim = False
if ('-a' in sys.argv):
	ax_lim = float(sys.argv[sys.argv.index('-a') + 1])
else:
	ax_lim_input = input("Axis limit (R_e): ")
	if ax_lim_input != "":
		ax_lim = float(ax_lim_input)
	else:
		ax_lim = -1
		assumed_ax_lim = True

if ('-n' in sys.argv):
	num_target_particles = int(sys.argv[sys.argv.index('-n') + 1])
else:
	num_target_particles_input = input("Number of target particles: ")
	if num_target_particles_input != "":
		num_target_particles = int(num_target_particles_input)
	else:
		num_target_particles = -1

find_recent = False
if ('-r' in sys.argv):
	find_recent = True
	sys.argv.remove('-r')

if ('-s' in sys.argv):
	start_index = int(sys.argv[sys.argv.index('-s') + 1])
else:
	start_index = 0

if ('-e' in sys.argv):
	end_index = int(sys.argv[sys.argv.index('-e') + 1])
else:
	end_index = -1

if ('-t' in sys.argv):
	time_step = float(sys.argv[sys.argv.index('-t') + 1])
else:
	time_step = -1

if ('-T0' in sys.argv):
	impact_time_shift = float(sys.argv[sys.argv.index('-T0') + 1])
else:
	impact_time_shift = 0.0

if ('-start' in sys.argv):
	simulation_time_shift = float(sys.argv[sys.argv.index('-start') + 1])
else:
	simulation_time_shift = 0.0

if ('-f' in sys.argv):
	final_output = True
else:
	final_output = False

if ('-cleanX' in sys.argv):
	x_axes = False
else:
	x_axes = True


if ('-cleanY' in sys.argv):
	y_axes = False
else:
	y_axes = True

#snapshot_path = "simulations/{0}/output/{0}_*.hdf5".format(snapshot_name)
snapshot_path = "/data/cluster4/hd20558/simulations/{0}/output/{0}_*.hdf5".format(simulation_name)

if final_output:
	extra_directory = "/final"
else:
	extra_directory = ""
output_path = "simulations/{0}{1}".format(simulation_name, extra_directory)

snapshots = glob.glob(snapshot_path)
snapshots.sort()

num_of_snapshots = len(snapshots)
oom = int(math.floor(math.log10(num_of_snapshots)))
snapshot_number_sig_fig = oom + 2

if os.path.exists(output_path) == False:
	os.makedirs(output_path)

if find_recent:
	images = glob.glob("{0}/*.png".format(output_path))
	start_index = len(images)

if end_index == -1: end_index = num_of_snapshots

for snapshot_id in range(start_index, end_index):
	pos, mat_id, ax_lim = snapshot.get_pos_mat_id(snapshots[snapshot_id], ax_lim, num_target_particles)

	if (assumed_ax_lim == True):
		print("Assuming axis limits of +- {0} R_e".format(ax_lim))
		assumed_ax_lim = False

	if time_step != -1:
		adjusted_time_step = (time_step * snapshot_id) - impact_time_shift + simulation_time_shift
	else:
		adjusted_time_step = "undefined"

	snapshot.plot_pos_mat_id(pos, mat_id, ax_lim, simulation_name, snapshot_id, adjusted_time_step, final_output, x_axes, y_axes)

	if final_output:
		additional_text = "_final"
	else:
		additional_text = ""

	output_name = "{0}/{1}_{2}{3}.png".format(output_path, simulation_name, str(snapshot_id).zfill(snapshot_number_sig_fig), additional_text)
	plt.savefig(output_name, dpi=100)
	plt.close()	
	print("Saved", output_name)
