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
## If the user wants to know the angle between the angular momentum and some reference vector (usually the normalised vector of the pre impact angular momentum) they can specify the vector here
if ('-ref' in sys.argv):
	reference = True
	reference_vector = np.asarray(sys.argv[sys.argv.index('-ref') + 1: sys.argv.index('-ref') + 4], dtype=float)
	print(reference_vector)
else:
	reference = False
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
if ('-r' in sys.argv):
	limit_radius = float(sys.argv[sys.argv.index('-r') + 1])
else:
	limit_radius = False

## Get the hdf5 data from the file they specified
## If the file needs to be run through the planet bound mass script then get the information from there, else just read it normally
if bound:
	remnants.main(sys.argv)

	pos, vel, h, m, rho, p, u, mat_id, R = custom_woma.bound_load_to_woma(filename, remnant_id)
else:
	pos, vel, h, m, rho, p, u, mat_id, R = custom_woma.load_to_woma(filename)



pos_r = np.sqrt(np.sum(pos**2, axis=1)) / R_earth 

com_truncate_mask = np.where(pos_r <= 25)[0]
temp_pos = pos[com_truncate_mask]
temp_m = m[com_truncate_mask]

com = np.sum(temp_m[:, np.newaxis] * temp_pos, axis=0) / (np.sum(temp_m))

pos -= com


if limit_radius:
	pos_r = np.sqrt(np.sum(pos**2, axis=1)) / R_earth
	mask = np.where(pos_r <= limit_radius)
	
	pos = pos[mask]
	vel = vel[mask]
	h = h[mask]
	m = m[mask]
	rho = rho[mask]
	p = p[mask]
	u = u[mask]
	mat_id = mat_id[mask]


## Compute and print the angular momentum from position, velocity, and mass via L = m(r x v)
L = np.sum(np.cross(pos, vel) * m[:, np.newaxis], axis=0)
print("\nAngular Momentum:")
print(L, "kg m^2 s^-1")

## Calculate and print the magnitude of the angular momentum
L_mag = np.sqrt(L[0]**2 + L[1]**2 + L[2]**2)
print(L_mag, "kg m^2 s^-1")

## Calculate and print the normalised angular momentum vector
L_norm = L / L_mag
print(L_norm)

## Compute the angle between the z axis vector and the angular momentum vector as projected into the xz plane, via the definition of the dot product: L . z = |L| |z| cos(theta)
projected_L = np.asarray([L[0], 0, L[2]])
projected_L_mag = np.sqrt(L[0]**2 + L[2]**2)
L_ang_from_z = math.acos(np.sum(projected_L * np.asarray([0, 0, 1])) / projected_L_mag) * 180 / math.pi

## This maps the angle of the dot product between L in the x,z plane and the z axis (which will be <90 degrees) to the angle from the +ve z axis
## as looking at the x,z plane from down the y axis, or towards negative y. (Such that +ve Z is to the right and +ve X is up)
## Negative angles mean the vector is pointing towards negative X, i.e. the vector is "below the z axis"
## Positive angles mean the vector is pointing towards positive X, i.e. the vector is "above the z axis"
if (L[0] < 0):
	L_ang_from_z *= -1


## Compute the angle between the y axis vector and the angular momentum vector, via the definition of the dot product: L . y = |L| |y| cos(theta)
## The angle from the y axis, which is like the angle theta in spherical coordinates
L_ang_from_y = math.acos(np.sum(L * np.asarray([0, 1, 0])) / L_mag) * 180 / math.pi


print("Looking down the y axis:")
print("( X")
print("  ^")
print("  |")
print(" (.)---> Z)\n")
print(L_ang_from_z, "degrees from z axis as projected into the x,z plane (-ve angle means pointing towards -ve X)")
print(L_ang_from_y, "degrees from y axis")

## Compute the angle from the reference vector if this was provided
if reference:
	L_ang_from_ref = math.acos(np.sum(L * reference_vector / L_mag)) * 180 / math.pi
	print("\nAngle from reference vector:")
	print(L_ang_from_ref, "degrees")
	print("Centre of mass found within 25 R_earth of box centre:")
	print(com / R_earth)


## Calculate and print the angular frequency in radians per second, and the period in hours
## I = mr^2
print("\nAngular Frequency and Period")
r2 = np.sum(pos**2, axis=1)	## This converts [[x_0, y_0, z_0], [x_1, y_1, z_1], ...] to [r_0^2, r_1^2, ...]
I = np.sum(m * r2)	# The total moment of inertia of an N body system is given by the sum of the moments of inertia of each of the particles

## The angular frequency is defined via the definition of the angular momentum (scalar), L = Iw
w = L_mag / I
period = 2 * math.pi / (w * 3600)
print(w, " rad s^-1")
print(period, "hours")


if limit_radius:
	extra_text = "_upto_{0}_Re".format(limit_radius)
else:
	extra_text = ""

## Write all of this data to a text file for ease of access, preventing the need to run this script repeatedly just to get a value that is required elsewhere
with open("{0}_angular_momentum{1}.txt".format(filename[:-5], extra_text), "w") as writer:
	writer.write("Script arguments:\n")
	writer.write("{0}\n\n".format(str(sys.argv)))

	writer.write("Angular Momentum\n")
	writer.write("{0}\t kg m^2 s^-1\n".format(L))
	writer.write("{0}\t\t\t\t\t kg m^2 s^-1\n".format(L_mag))
	writer.write("{0}\t normalised\n\n".format(L_norm))

	writer.write("Looking down the y axis:\n")
	writer.write("( X\n")
	writer.write("  ^\n")
	writer.write("  |\n")
	writer.write(" (.)---> Z)\n\n")

	writer.write("{0} degrees from z axis as projected into the x,z plane (-ve angle means pointing towards -ve X)\n".format(L_ang_from_z))
	writer.write("{0} degrees from y axis\n".format(L_ang_from_y))

	if reference:
		writer.write("\nAngle from reference vector: ({0})\n".format(str(reference_vector)))
		writer.write("{0} degrees\n".format(L_ang_from_ref))
		writer.write("\nCentre of Mass:\n")
		writer.write(str(com / R_earth))


	writer.write("\nAngular Frequency and Period\n")
	writer.write("{0} rad s^-1\n".format(w))
	writer.write("{0} hours".format(period))



	


