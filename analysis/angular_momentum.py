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
#
#
##
if ('-mat' in sys.argv):
	material = int(sys.argv[sys.argv.index('-mat') + 1])
else:
	material = False


## Get the hdf5 data from the file they specified
## If the file needs to be run through the planet bound mass script then get the information from there, else just read it normally
if bound:
	remnants.main(sys.argv)

	pos, vel, h, m, rho, p, u, mat_id, R = custom_woma.bound_load_to_woma(filename, remnant_id)
else:
	pos, vel, h, m, rho, p, u, mat_id, R = custom_woma.load_to_woma(filename)


## Offset particles such that centre of mass is at the origin
pos_r = np.sqrt(np.sum(pos**2, axis=1))
	## Calculate centre of mass from particles within 25 Earth radii of origin
com_truncate_mask = np.where(pos_r <= 25 * R_earth)[0]
temp_pos = pos[com_truncate_mask]
temp_m = m[com_truncate_mask]

com = np.sum(temp_m[:, np.newaxis] * temp_pos, axis=0) / (np.sum(temp_m))

pos -= com


## Mask out particles that are outside the region requested by the user
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


## Mask out the particles that match the material requested by the user
if material:
	if material == -1:
		print(set(mat_id))
		material = int(input("Enter material id: "))

	mask = np.where(mat_id == material)[0]

	pos = pos[mask]
	pos_r = pos_r[mask]
	vel = vel[mask]
	h = h[mask]
	m = m[mask]
	rho = rho[mask]
	p = p[mask]
	u = u[mask]
	mat_id = mat_id[mask]


## Compute and print the angular momentum from position, velocity, and mass via L = m(r x v)
L = np.sum(np.cross(pos, vel) * m[:, np.newaxis], axis=0)
#print(m)
#print(vel)
#print(m[:, np.newaxis] * vel)

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
		
## The angular velocity is defined via the definition of the angular momentum (scalar), L = Iw
angular_speed = L_mag / I

period = 2 * math.pi / (angular_speed * 3600)

print(angular_speed, "rad s^-1")
print(period, "hours")

## Calculate the contraction effects if there is material out beyond 3.98 Earth radii, and if we haven't masked out a single material type
if upper_radius > 3.98 and not material:
	extended_atmosphere_mask = np.where(r2 >= (3.98 * R_earth)**2)[0]

	extended_atmosphere_pos = pos[extended_atmosphere_mask]
	extended_atmosphere_r2 = np.sum(extended_atmosphere_pos**2, axis=1) 
	extended_atmosphere_r = np.sqrt(extended_atmosphere_r2)


	sort = np.argsort(extended_atmosphere_r2)
	extended_atmosphere_pos_sorted = extended_atmosphere_pos[sort]
	extended_atmosphere_r2_sorted = extended_atmosphere_r2[sort]
	extended_atmosphere_r_sorted = np.sqrt(extended_atmosphere_r2_sorted)

	#print(extended_atmosphere_r_sorted[-1] / R_earth)

	extended_atmosphere_r -= 3.98 * R_earth
	extended_atmosphere_r *= R_earth/(extended_atmosphere_r_sorted[-1] - extended_atmosphere_r_sorted[0])
	extended_atmosphere_r += 2.98 * R_earth

	#sort = np.argsort(extended_atmosphere_r)
	#extended_atmosphere_r_sorted = extended_atmosphere_r[sort]
	#print(extended_atmosphere_r_sorted[-1] / R_earth)


	original_r2 = np.copy(r2)
	#r2 *= (2.98/3.98)**2
	r2[extended_atmosphere_mask] = extended_atmosphere_r**2

	adjusted_I = np.sum(m * r2)

	adjusted_angular_speed = L_mag / adjusted_I

	adjusted_period_atmospheric_contraction = 2 * math.pi / (adjusted_angular_speed * 3600)

	print("Accounting for thermal contraction to 3.98 R_earth (atmospheric contraction):")
	print(adjusted_angular_speed, "rad s^-1")
	print(adjusted_period_atmospheric_contraction, "hours")



	r2 = original_r2
	r2 *= (2.98/3.98)**2
	r2[extended_atmosphere_mask] = extended_atmosphere_r**2

	adjusted_I = np.sum(m * r2)

	adjusted_angular_speed = L_mag / adjusted_I

	adjusted_period_total_contraction = 2 * math.pi / (adjusted_angular_speed * 3600)

	print("Accounting for thermal contraction to 3.98 R_earth (total contraction):")
	print(adjusted_angular_speed, "rad s^-1")
	print(adjusted_period_total_contraction, "hours")


if lower_radius or upper_radius:
	extra_text = "_from_{0}_upto_{1}_Re".format(lower_radius, upper_radius)
else:
	extra_text = ""

if material:
	extra_text = "_mat_{0}{1}".format(material, extra_text)

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
		writer.write("Centre of Mass:\n")
		writer.write(str(com / R_earth) + "\n")


	writer.write("\nAngular Frequency and Period\n")
	writer.write("{0} rad s^-1\n".format(angular_speed))
	writer.write("{0} hours\n\n".format(period))

	if upper_radius > 3.98 and not material:
		writer.write("Atmospheric Contraction\n")
		writer.write("{0} hours \n\n".format(adjusted_period_atmospheric_contraction))

		writer.write("Total Contraction\n")
		writer.write("{0} hours \n\n".format(adjusted_period_total_contraction))



if lower_radius or upper_radius:
	with open("{0}_ang_mom_values.txt".format(filename[:-5], extra_text), "a") as writer:
		if not reference:
			L_ang_from_ref = 0

		writer.write("{0},{1},{2},{3}\n".format(lower_radius, upper_radius, L_ang_from_ref, period))

	


