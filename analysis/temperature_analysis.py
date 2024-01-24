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


def plot_radius(positions):
	radii = []
	for snapshot in positions:
		snapshotArray = snapshot.astype(np.float64)
		radius = float((snapshotArray.max() - snapshotArray.min()).to_value()) / 2
		radii.append(radius)
	
	plt.figure(figsize=(10,10))
	ax = plt.gca()

	plt.plot(np.linspace(0, len(radii) * 300, len(radii)), radii)

	plt.ylabel(r"Radius [$R_\oplus$]")
	plt.xlabel("Time [s]")
	plt.savefig("visualised/analysis/Radius_vs_time.png")
	plt.close()
	
	

if (len(sys.argv) > 1):
	simulation_name = sys.argv[1]
else:
	simulation_name = input("Enter the name of the simulation: ")

#assumed_ax_lim = True
#if (len(sys.argv) > 2):
#	ax_lim = float(sys.argv[2])
#else:
#	ax_lim_input = input("Axis limit (R_e): ")
#	if ax_lim_input != "":
#		ax_lim = float(ax_lim_input)
#		assumed_ax_lim = False
#	else:
#		ax_lim = -1

snapshot_path = "/data/cluster4/hd20558/simulations/{0}/output/{0}_*.hdf5".format(simulation_name)
output_path = "/home/hd20558/files/simulations/{0}/analysis/".format(simulation_name)

snapshots = glob.glob(snapshot_path)
snapshots.sort()

num_of_snapshots = len(snapshots)
oom = int(math.floor(math.log10(num_of_snapshots)))
snapshot_number_sig_fig = oom + 2

if os.path.exists(output_path) == False:
	os.makedirs(output_path)

woma.load_eos_tables()

temperatures = []
for snapshot_id in range(num_of_snapshots):

	pos, vel, h, m, rho, p, u, mat_id, R = custom_woma.load_to_woma(snapshots[snapshot_id])
	temperatures.append(woma.eos.eos.A1_T_u_rho(u, rho, mat_id))

print(temperatures[-1])