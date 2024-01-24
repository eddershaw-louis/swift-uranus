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

#	       M_t      M_i     R_t    R_i   B    r                target_file                                impactor_file
PARAMETERS = [13.566, 0.99917, 3.98, 1.5702, 25, 22, "pre_damping_uranus_-1M_relaxation_0048.hdf5", "pre_damping_1M_relaxation_v1_1_long_1000.hdf5"]


M_t = PARAMETERS[0] * M_earth
M_i = PARAMETERS[1] * M_earth
R_t = PARAMETERS[2] * R_earth
R_i = PARAMETERS[3] * R_earth
B = PARAMETERS[4]
separation = PARAMETERS[5] * R_earth
target_filename = PARAMETERS[6]
impactor_filename = PARAMETERS[7]
target_filepath = "impact_files/{0}".format(target_filename)
impactor_filepath = "impact_files/{0}".format(impactor_filename)

v_esc = np.sqrt(2 * G * (M_t + M_i) / (R_t + R_i))
print("v_esc", v_esc)

A1_pos_t = np.array([0., 0., 0.])
A1_vel_t = np.array([0., 0., 0.])

A1_pos_i, A1_vel_i = woma.impact_pos_vel_b_v_c_r(
    b       = np.sin(B * np.pi/180), 
    v_c     = v_esc, 
    r       = separation, 
    R_t     = R_t, 
    R_i     = R_i, 
    M_t     = M_t, 
    M_i     = M_i,
)


# Centre of mass
A1_pos_com = (M_t * A1_pos_t + M_i * A1_pos_i) / (M_t + M_i)
A1_pos_t -= A1_pos_com
A1_pos_i -= A1_pos_com

# Centre of momentum
A1_vel_com = (M_t * A1_vel_t + M_i * A1_vel_i) / (M_t + M_i)
A1_vel_t -= A1_vel_com
A1_vel_i -= A1_vel_com

print("New Target Positions:")
print(A1_pos_t / R_earth, "R_earth")
print("New Target Velocities")
print(A1_vel_t, "m/s")

print("\nNew Impactor Positions:")
print(A1_pos_i / R_earth, "R_earth")
print("New Impactor Velocities")
print(A1_vel_i, "m/s\n\n")



pos_t, vel_t, h_t, m_t, rho_t, p_t, u_t, matid_t, R_t = custom_woma.load_to_woma(
    target_filepath
)
pos_i, vel_i, h_i, m_i, rho_i, p_i, u_i, matid_i, R_i = custom_woma.load_to_woma(
    impactor_filepath
)

#print(vel_t)

rot_period_t = 20 	#hours
ang_vel_t_scalar = 1 / (rot_period_t * 3600) 	#s^-1

#Assumes that the z axis is along the post impact axis of rotation, so the pre-impact axis of rotation should be
#~98 degrees from the z axis (towards y)
#I might simplify this to 90 degrees and have the pre-impact spin be around the y axis

rot_axis_ang_t = 98 #degrees

#R_x = 	[1		0		0
#	 0		cos(theta)	-sin(theta)
#	 0		sin(theta)	cos(theta)]
#
#Initial rotation is around the z axis, we then rotate around the x axis
# which pushes the axis of rotation from z towards y
#
#pos_t_T = pos_t.T
#
#dist_from_z = np.sqrt(pos_t_T[0]**2 + pos_t_T[1]**2)
#angle_around_z = np.arctan2(pos_t_T[1], pos_t_T[0])
#
#print(dist_from_z[:, np.newaxis])
#print(angle_around_z[:, np.newaxis])
#
#rot_vel_t_x = dist_from_z[:, np.newaxis] * np.cos(angle_around_z)[:, np.newaxis] * ang_vel_t_scalar
#rot_vel_t_y = dist_from_z[:, np.newaxis] * np.sin(angle_around_z)[:, np.newaxis] * ang_vel_t_scalar
#rot_vel_t_z = np.zeros(len(rot_vel_t_x))
#
#print(rot_vel_t_x)
#print(rot_vel_t_y)
#
# TODO: Apply rotation matrix to rotate these about the x axis
#
#r w cos(phi) = v_x
#r w sin(phi) = v_y

mask_above_hemisphere_plane = np.where(A1_pos_t[:, 1] >= math.tan(180 - rot_axis_ang_t) , True, False)
mask_below_hemisphere_plane = ~mask_above_hemisphere_plane

rim_speed = ang_vel_t_scalar * R_t
hemisphere_speed_offset = rim_speed / 4


pos_t += A1_pos_t
vel_t[:] += A1_vel_t

pre_rotation = true
if pre_rotation:
	vel_t[mask_above_hemisphere_plane, 0] += hemisphere_speed_offset
	vel_t[mask_below_hemisphere_plane, 0] -= hemisphere_speed_offset

pos_i += A1_pos_i
vel_i[:] += A1_vel_i


with h5py.File("impact_files/IMPACT--{0}--{1}".format(target_filename[:-5], impactor_filename), "w") as f:
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