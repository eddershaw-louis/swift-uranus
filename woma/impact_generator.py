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

import womaplotting
import woma
import h5py
import numpy as np
import os
import swiftsimio as sw
import unyt
import sys

R_earth = 6.371e6   # m
M_earth = 5.9724e24  # kg
G = 6.67408e-11  # m^3 kg^-1 s^-2

sys.path.append("..")
sys.path.append("../..")

from custom_functions import custom_woma

#	       M_t       M_i    R_t   R_i    B   r   v                 target_file                   impactor_file
#PARAMETERS = [14.044, 0.49996, 3.98, 1.1605, 30, 22, 1.0,  "hotel_spinning_uranus_0.5M_r158.hdf5", "impactor_0.5M.hdf5"]
#PARAMETERS = [13.974, 0.59978, 3.98, 1.2218, 30, 22, 1.0,  "hotel_spinning_uranus_0.6M_r158.hdf5", "impactor_0.6M.hdf5"]
#PARAMETERS = [13.899, 0.69967, 3.98, 1.2756, 30, 22, 1.0,  "hotel_spinning_uranus_0.7M_r158.hdf5", "impactor_0.7M.hdf5"]
#PARAMETERS = [13.836, 0.74997, 3.98, 1.3002, 30, 22, 1.0, "hotel_spinning_uranus_0.75M_r158.hdf5", "impactor_0.75M.hdf5"]
PARAMETERS = [13.732, 0.87435, 3.98, 1.3567, 30, 22, 1.0, "hotel_spinning_uranus_0.875M_r138.hdf5", "impactor_0.875M.hdf5"]
#PARAMETERS = [13.591, 0.99962, 3.98, 1.4073, 30, 22, 1.0,    "hotel_spinning_uranus_1M_r158.hdf5", "impactor_1M.hdf5"]
#PARAMETERS = [13.444, 1.1243,  3.98, 1.4529, 30, 22, 1.0,"hotel_spinning_uranus_1.125M_r158.hdf5", "impactor_1.125M.hdf5"]
#PARAMETERS = [13.325, 1.2493,  3.98, 1.4947, 30, 22, 1.0, "hotel_spinning_uranus_1.25M_r158.hdf5", "impactor_1.25M.hdf5"]
#PARAMETERS = [13.055, 1.4999,  3.98, 1.5692, 30, 22, 1.0,  "hotel_spinning_uranus_1.5M_r158.hdf5", "impactor_1.5M.hdf5"]
#PARAMETERS = [12.825, 1.7499,  3.98, 1.6327, 30, 22, 1.0, "hotel_spinning_uranus_1.75M_r158.hdf5", "impactor_1.75M.hdf5"]
#PARAMETERS = [12.577, 1.9983,  3.98, 1.6893, 30, 22, 1.0,    "beta_spinning_uranus_2M_r148.hdf5", "impactor_2M.hdf5"]

## Read in parameters
M_t = PARAMETERS[0] * M_earth
M_i = PARAMETERS[1] * M_earth
R_t = PARAMETERS[2] * R_earth
R_i = PARAMETERS[3] * R_earth
B = PARAMETERS[4]
separation = PARAMETERS[5] * R_earth
v_esc_multiplier = PARAMETERS[6]
target_filename = PARAMETERS[7]
impactor_filename = PARAMETERS[8]
target_filepath = "impact_files/{0}".format(target_filename)
impactor_filepath = "impact_files/{0}".format(impactor_filename)

## Calculate the mutual escape velocity
v_esc = np.sqrt(2 * G * (M_t + M_i) / (R_t + R_i)) 
print("v_esc", v_esc)
v_c = v_esc_multiplier * v_esc
print("Contact velocity", v_c, "\n")

impact_pos_t = np.array([0., 0., 0.])
impact_vel_t = np.array([0., 0., 0.])

## Compute the initial configuration that satisfies the impact parameters
impact_pos_i, impact_vel_i = woma.impact_pos_vel_b_v_c_r(
    b       = np.sin(B * np.pi/180), 
    v_c     = v_c, 
    r       = separation, 
    R_t     = R_t, 
    R_i     = R_i, 
    M_t     = M_t, 
    M_i     = M_i,
)


# Centre of mass
impact_pos_com = (M_t * impact_pos_t + M_i * impact_pos_i) / (M_t + M_i)

## Offset bodies such that the origin is the centre of mass
impact_pos_t -= impact_pos_com
impact_pos_i -= impact_pos_com


# Centre of momentum
impact_vel_com = (M_t * impact_vel_t + M_i * impact_vel_i) / (M_t + M_i)

## Offset the velocities of the bodies such that the origin is the centre of momentum
impact_vel_t -= impact_vel_com
impact_vel_i -= impact_vel_com


print("New Target Position:")
print(impact_pos_t / R_earth, "R_earth")
print("New Target Velocity:")
print(impact_vel_t, "m/s")

print("\nNew Impactor Position:")
print(impact_pos_i / R_earth, "R_earth")
print("New Impactor Velocity:")
print(impact_vel_i, "m/s")
print(np.linalg.norm(impact_vel_i), "m/s\n")

print("Centre of momentum", impact_vel_com, "m/s")
print(np.linalg.norm(impact_vel_com), "m/s\n")


print("Impactor Approach Velocity Relative to Target:")
print(np.linalg.norm(impact_vel_i) - np.linalg.norm(impact_vel_com), "m/s\n\n")


## Load in particles from hdf5 files
pos_t, vel_t, h_t, m_t, rho_t, p_t, u_t, matid_t, R_t = custom_woma.load_to_woma(target_filepath)
pos_i, vel_i, h_i, m_i, rho_i, p_i, u_i, matid_i, R_i = custom_woma.load_to_woma(impactor_filepath)


## Offset each bodies' particles' position and velocities to the right values
pos_t += impact_pos_t
vel_t[:] += impact_vel_t

pos_i += impact_pos_i
vel_i[:] += impact_vel_i


## Save the impact configuration
with h5py.File("impact_files/IMPACT--b{0}--{1}--{2}".format(B, target_filename[:-5], impactor_filename), "w") as f:
	woma.save_particle_data(
        	f,
        	np.append(pos_t, pos_i, axis=0),
        	np.append(vel_t, vel_i, axis=0),
       		np.append(m_t, m_i),
        	np.append(h_t, h_i),
        	np.append(rho_t, rho_i),
        	np.append(p_t, p_i),
        	np.append(u_t, u_i),
        	np.append(matid_t, matid_i),
        	boxsize=500 * R_earth,
        	file_to_SI=woma.Conversions(M_earth, R_earth, 1),
    )