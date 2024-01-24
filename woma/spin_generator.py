import womaplotting
import woma
import h5py
import numpy as np
import os
import swiftsimio as sw
import unyt
import sys
import math

R_earth = 6.371e6   # m
M_earth = 5.9724e24  # kg
G = 6.67408e-11  # m^3 kg^-1 s^-2

sys.path.append("..")
sys.path.append("../..")

from custom_functions import custom_woma

if (len(sys.argv) > 1):
	target_filepath = sys.argv[1]
else:
	target_filepath = input("Enter filepath to hdf5 file to spin up: ")

target_filename = ""
for i in range(1, len(target_filepath)):
	if target_filepath[-i] == "/":
		target_filename = target_filepath[-i + 1:-5]

if target_filename == "":
	raise Exception("Unable to find file!")

if ('-P' in sys.argv):
	rot_period_t = float(sys.argv[sys.argv.index('-P') + 1])
else:
	rot_period_t = float(input("Enter period of rotation of planet (in hours): "))


pos_t, vel_t, h_t, m_t, rho_t, p_t, u_t, matid_t, R_t = custom_woma.load_to_woma(
    target_filepath
)

#print(vel_t)

ang_vel_t_scalar = 2 * math.pi / (rot_period_t * 3600) 	#s^-1

#Assumes that the z axis is along the post impact axis of rotation, so the pre-impact axis of rotation should be
#~98 degrees from the z axis (towards y)
#I might simplify this to 90 degrees and have the pre-impact spin be around the y axis

rot_axis_ang_t = 98 #degrees

mask_above_hemisphere_plane = np.where(pos_t[:, 1] >= math.tan(180 - rot_axis_ang_t) * pos_t[:, 2], True, False)
mask_below_hemisphere_plane = ~mask_above_hemisphere_plane

unique, counts = np.unique(mask_above_hemisphere_plane, return_counts=True)

print(dict(zip(unique, counts)))


rim_speed = ang_vel_t_scalar * R_t
hemisphere_speed_offset = rim_speed / 1

print(hemisphere_speed_offset)

vel_t[mask_above_hemisphere_plane, 0] += hemisphere_speed_offset
vel_t[mask_below_hemisphere_plane, 0] -= hemisphere_speed_offset


with h5py.File("spinning_files/{0}-spun-up.hdf5".format(target_filename), "w") as f:
	woma.save_particle_data(
        	f,
        	pos_t,
        	vel_t,
       		m_t,
        	h_t,
        	rho_t,
        	p_t,
        	u_t,
        	matid_t,
        	boxsize=500 * R_earth,
        	file_to_SI=woma.Conversions(M_earth, R_earth, 1),
    )