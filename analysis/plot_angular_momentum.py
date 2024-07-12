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
#import math
import sys
import csv


sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")

#import woma
#from custom_functions import custom_woma
#from custom_functions import material_colour_map

font_size = 18
params = {
	"font.size": font_size,
	"axes.labelsize": 1.2 * font_size,
	"xtick.labelsize": font_size,
	"ytick.labelsize": font_size,
	"font.family": "serif",
}
matplotlib.rcParams.update(params)


R_earth = 6.371e6   # m

## Get the filepath of the hdf5 file to analyse
if (len(sys.argv) > 1):
	filename = sys.argv[1]
else:
	filename = input("Filepath of angular momenta .txt file to analyse (include .txt suffix): ")

if ('-ref' in sys.argv):
	reference_filename = sys.argv[sys.argv.index('-ref') + 1]
else:
	reference_filename = False


lower_radii = []
upper_radii = []
axial_tilts = []
periods = []

with open(filename, newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	
	for row in reader:
		lower_radii.append(float(row[0]))
		upper_radii.append(float(row[1]))
		axial_tilts.append(float(row[2]))
		periods.append(float(row[3]))



if reference_filename:
	ref_lower_radii = []
	ref_upper_radii = []
	ref_axial_tilts = []
	ref_periods = []

	with open(reference_filename, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
	
		for row in reader:
			ref_lower_radii.append(float(row[0]))
			ref_upper_radii.append(float(row[1]))
			ref_axial_tilts.append(0)
			ref_periods.append(float(row[3]))


	

	
#print(axial_tilts)
#print(periods)

fig, ax = plt.subplots()
#ax.set_aspect("equal")


ax.scatter(upper_radii, axial_tilts, color="tab:blue", alpha=1, label="Post Impact")
ax.plot(upper_radii, 97.7 * np.ones(len(axial_tilts)), linestyle="dashed", color="black")

ax.set_xlabel(r"Radius [R$_\oplus$]")
ax.set_ylabel(r"Axial Tilt [deg]")

if reference_filename:
	ax.scatter(ref_upper_radii, ref_axial_tilts, marker="x", color="tab:blue", alpha=1, label="Pre Impact")

ax.set_ylim(-5, 105)

#ax.legend(fontsize="small", loc=2)


plt.tight_layout()

plt.savefig("{0}_axial_tilt_upper_radii.png".format(filename[:-4]))
plt.close()


fig, ax = plt.subplots()
#ax.set_aspect("equal")


ax.scatter(upper_radii, periods, color="tab:red", alpha=1, label="Post Impact")
ax.plot(upper_radii, 17.23 * np.ones(len(axial_tilts)), linestyle="dashed", color="black")


ax.set_xlabel(r"Radius [R$_\oplus$]")
ax.set_ylabel(r"Period [hrs]")

if reference_filename:
	ax.scatter(ref_upper_radii, ref_periods, marker="x", color="tab:red", alpha=1, label="Pre Impact")

ax.set_ylim(-5, 105)

#ax.legend(fontsize="small", loc=2)


plt.tight_layout()

plt.savefig("{0}_period_upper_radii.png".format(filename[:-4]))
plt.close()


quit()



fig, ax = plt.subplots()
#ax.set_aspect("equal")

ax2 = ax.twinx()

plot1 = ax.scatter(upper_radii, axial_tilts, color="tab:blue", alpha=0.7)

ax.set_xlabel(r"Radius [R$_\oplus$]")
ax.set_ylabel(r"Axial Tilt [degrees]")

plot2 = ax2.scatter(upper_radii, periods, color="tab:red", alpha=0.7)

ax2.set_ylabel(r"Period [hours]")


if reference_filename:
	ref_lower_radii = []
	ref_upper_radii = []
	ref_axial_tilts = []
	ref_periods = []

	with open(reference_filename, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
	
		for row in reader:
			ref_lower_radii.append(float(row[0]))
			ref_upper_radii.append(float(row[1]))
			ref_axial_tilts.append(0)
			ref_periods.append(float(row[3]))


	plot3 = ax.scatter(upper_radii, ref_axial_tilts, marker="x", color="tab:blue", alpha=0.7)
	plot4 = ax2.scatter(upper_radii, ref_periods, marker="x", color="tab:red",  alpha=0.7)

	plots = [plot1, plot2, plot3, plot4]
else:
	plots = [plot1, plot2]

x_lims = ax.get_xlim()
y_lims = ax2.get_ylim()

ax.set_xlim(x_lims[0], x_lims[1])
ax2.set_ylim(-y_lims[1] * 0.05, y_lims[1])

ax.set_ylim(-5, 100)

plot_tilt_legend = ax.plot(-1, 180, color="tab:blue", label="Tilt")
plot_period_legend = ax.plot(-1, 0, color="tab:red", label="Period")

#print(plots)
#plots.append(plot_tilt_legend)
#plots.append(plot_period_legend)
#print(plots)

#labels = [l.get_label() for l in plots]
ax.legend(fontsize="small", loc=2)


plt.tight_layout()

plt.savefig("{0}_upper_radii.png".format(filename[:-4]))
plt.close()