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

import glob
import os



beta_folders = glob.glob("simulations/hotel_impact_spinning_1.75M*/")
beta_folders.sort()

#print(beta_folders)

for folder in beta_folders:
	simulation_name = folder[12:-1]
	print(simulation_name)

	simulation_files = glob.glob("/home/hd20558/scratch_space/{0}/output/*.hdf5".format(simulation_name))
	if len(simulation_files) > 0:
		simulation_files.sort()
		os.system("cp {0} {1}.".format(simulation_files[-1], folder))

	#input("Press Enter to fetch next simulation")