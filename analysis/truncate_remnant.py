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

import numpy as np
import math
import sys
import h5py
import matplotlib.pyplot as plt

import os

sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")

import woma
from custom_functions import custom_woma
from custom_functions import material_colour_map

R_earth = 6.371e6   # m
M_earth = 5.9724e24  # kg

## Get the filepath of the hdf5 file to analyse
if (len(sys.argv) > 1):
	filename = sys.argv[1]
else:
	filename = input("Filepath of .hdf5 file to analyse (include .hdf5 suffix): ")
	sys.argv.insert(filename, 1)

if (len(sys.argv) > 2):
	truncation_radius_Re = float(sys.argv[2])
else:
	truncation_radius_Re = float(input("Radius to truncate particles to (R_earth): ")) 


##					       REMEMBER THIS!
##						\~~~~~~~~~~/
##						 \~~~~~~~~/
##						  \~~~~~~/
truncation_radius = truncation_radius_Re * R_earth #* 1.05
##						  /~~~~~~\
##						 /~~~~~~~~\
##						/~~~~~~~~~~\
##				Added for the density floor catchment radius!



pos, vel, h, m, rho, p, u, mat_id, R = custom_woma.load_to_woma(filename)


pos_r = np.sqrt(np.sum(pos**2, axis=1)) / R_earth 

com_truncate_mask = np.where(pos_r <= 15)[0]
temp_pos = pos[com_truncate_mask]
temp_m = m[com_truncate_mask]

com = np.sum(temp_m[:, np.newaxis] * temp_pos, axis=0) / (np.sum(temp_m))

pos -= com

box_centre = 250
pos_r = np.sqrt(np.sum(pos**2, axis=1))



mask = np.where((pos_r <= truncation_radius))[0]
print(mask)
print(len(mask))
print(truncation_radius)


pos_tr = pos[mask]
vel_tr = vel[mask]
h_tr = h[mask]
m_tr = m[mask]
rho_tr = rho[mask]
p_tr = p[mask]
u_tr = u[mask]
mat_id_tr = mat_id[mask]


with h5py.File("{0}_truncated.hdf5".format(filename[:-5], truncation_radius_Re), "w") as f:
	woma.save_particle_data(
        	f,
        	pos_tr,
        	vel_tr,
       		m_tr,
        	h_tr,
        	rho_tr,
        	p_tr,
        	u_tr,
        	mat_id_tr,
        	boxsize=500 * R_earth,
        	file_to_SI=woma.Conversions(M_earth, R_earth, 1),
    )


#plt.scatter(pos_tr[:, 0], pos_tr[:, 1])
#plt.show()
#plt.close()


os.makedirs("{0}_truncated_{1}/output/".format(filename[:-5], truncation_radius_Re))
os.system("cp {0}_truncated.hdf5 {0}_truncated_{1}/truncated.hdf5".format(filename[:-5], truncation_radius_Re))
os.system("cp truncated.yml {0}_truncated_{1}/truncated.yml".format(filename[:-5], truncation_radius_Re))









	


