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



import glob
import sys
import os
import math

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
	plt.savefig("Radius_vs_time.png")
	plt.close()
	
	

if (len(sys.argv) > 1):
	simulation_name = sys.argv[1]
else:
	simulation_name = input("Enter the name of the simulation: ")

assumed_ax_lim = False
if (len(sys.argv) > 1):
	ax_lim = float(sys.argv[2])
else:
	ax_lim_input = input("Axis limit (R_e): ")
	if ax_lim_input != "":
		ax_lim = float(ax_lim_input)
	else:
		ax_lim = -1
		assumed_ax_lim = True

#snapshot_name = os.path.abspath('.')[len(os.path.abspath('..')) + 1:]
snapshot_path = "/data/cluster4/hd20558/simulations/{0}/output/{0}_*.hdf5".format(simulation_name)
output_path = "simulations/{0}/".format(simulation_name)

snapshots = glob.glob(snapshot_path)
snapshots.sort()

num_of_snapshots = len(snapshots)
oom = int(math.floor(math.log10(num_of_snapshots)))
snapshot_number_sig_fig = oom + 2

if os.path.exists(output_path) == False:
	os.makedirs(output_path)

positions = []
for snapshot_id in range(num_of_snapshots):
	pos, mat_id, ax_lim = snapshot.get_pos_mat_id(snapshots[snapshot_id], ax_lim, -1)
	if (assumed_ax_lim == True):
		print("Assuming axis limits of +- {0} R_e".format(ax_lim))
		assumed_ax_lim = False
	
	positions.append(pos)
plot_radius(positions)