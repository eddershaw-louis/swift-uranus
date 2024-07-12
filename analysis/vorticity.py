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

import remnants
import matplotlib.pyplot as plt
import numpy as np
import math
import sys


sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")

import woma
from custom_functions import custom_woma
from custom_functions import material_colour_map

R_earth = 6.371e6   # m

## Get the filepath of the hdf5 file to analyse
if (len(sys.argv) > 1):
	filename = sys.argv[1]
else:
	filename = input("Filepath of .hdf5 file to analyse (include .hdf5 suffix): ")
	sys.argv.insert(filename, 1)
#
#
## If the hdf5 file needs to be run through the planet bound mass script to extract particles that are part of a single remnant then the user should specify this, as well as which remnant they want to analyse
if ('-b' in sys.argv):
	bound = True
	remnant_id = int(sys.argv[sys.argv.index('-b') + 1])
else:
	bound = False
#
#
##
if ('-lr' in sys.argv):
	lower_radius = float(sys.argv[sys.argv.index('-lr') + 1])
else:
	lower_radius = 0
#
#
##
if ('-ur' in sys.argv):
	upper_radius = float(sys.argv[sys.argv.index('-ur') + 1])
else:
	upper_radius = False


## Get the hdf5 data from the file they specified
## If the file needs to be run through the planet bound mass script then get the information from there, else just read it normally
if bound:
	remnants.main(sys.argv)

	pos, vel, h, m, rho, p, u, mat_id, R = custom_woma.bound_load_to_woma(filename, remnant_id)
else:
	pos, vel, h, m, rho, p, u, mat_id, R = custom_woma.load_to_woma(filename)



pos_r = np.sqrt(np.sum(pos**2, axis=1))

com_truncate_mask = np.where(pos_r <= 25 * R_earth)[0]
temp_pos = pos[com_truncate_mask]
temp_m = m[com_truncate_mask]

com = np.sum(temp_m[:, np.newaxis] * temp_pos, axis=0) / (np.sum(temp_m))

pos -= com


if lower_radius or upper_radius:
	pos_r = np.sqrt(np.sum(pos**2, axis=1))
	if upper_radius:
		mask = np.where(pos_r <= upper_radius * R_earth)[0]
	else:
		mask = np.where(pos_r >= lower_radius * R_earth)[0]

	
	pos = pos[mask]
	pos_r = pos_r[mask]
	vel = vel[mask]
	h = h[mask]
	m = m[mask]
	rho = rho[mask]
	p = p[mask]
	u = u[mask]
	mat_id = mat_id[mask]


print(np.shape(pos))
print(np.shape(pos.T))

print(np.shape(vel))

vel_x = vel[:, 0]
vel_y = vel[:, 1]
vel_z = vel[:, 2]
print(np.gradient(vel_x, pos[:, 0]))
quit()



if lower_radius or upper_radius:
	extra_text = "_from_{0}_upto_{1}_Re".format(lower_radius, upper_radius)
else:
	extra_text = ""

## Write all of this data to a text file for ease of access, preventing the need to run this script repeatedly just to get a value that is required elsewhere
with open("{0}_vorticity{1}.txt".format(filename[:-5], extra_text), "w") as writer:
	writer.write("Script arguments:\n")
	writer.write("{0}\n\n".format(str(sys.argv)))
	


