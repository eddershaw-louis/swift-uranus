import remnants
import matplotlib.pyplot as plt
import numpy as np
import math
import sys

sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")
sys.path.append("../../../..")

import woma
from custom_functions import custom_woma

if (len(sys.argv) >= 2):
	filename = sys.argv[1]
else:
	filename = input("Name of HDF5 file to analyse: ")
	sys.argv.append(filename)

remnants.main(sys.argv)

remnant_pos, remnant_vel, remnant_h, remnant_m, remnant_rho, remnant_p, remnant_u, remnant_matid, remnant_R = custom_woma.bound_load_to_woma(sys.argv[1], 1)

remnant_L = np.sum(np.cross(remnant_pos, remnant_vel) * remnant_m[:, np.newaxis], axis=0)

print("\nAngular Momentum:")
print(remnant_L, "kg m^2 s^-1")
remnant_L_mag = np.sqrt(remnant_L[0]**2 + remnant_L[1]**2 + remnant_L[2]**2)
print(remnant_L_mag, "kg m^2 s^-1")

remnant_L_dir = math.acos(np.sum(remnant_L * np.asarray([0, 0, 1])) / remnant_L_mag) * 180 / math.pi
print(remnant_L_dir, "degrees")
#print(np.sqrt(remnant_L_dir[0]**2 + remnant_L_dir[1]**2 + remnant_L_dir[2]**2))


print("\nAngular Frequency and Period")
remnant_r2 = np.sum(remnant_pos**2, axis=1)
remnant_I = np.sum(remnant_m * remnant_r2)

remnant_w = remnant_L_mag / remnant_I
print(remnant_w, " rad s^-1")
print(2 * math.pi / (remnant_w * 3600), "hours")


