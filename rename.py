## Rename
import sys
import os
import glob

simulation_base_filepath = "/data/cluster4/hd20558/simulations"
visualised_base_filepath = "/home/hd20558/files/simulations"

if (len(sys.argv) > 1):
	simulation_name_old = sys.argv[1]
else:
	simulation_name_old = input("Enter the name of the simulation to rename: ")

simulation_filepath_old = "{0}/{1}".format(simulation_base_filepath, simulation_name_old)

if (len(sys.argv) > 2):
	simulation_name_new = sys.argv[2]
else:
	simulation_name_new = input("Enter the NEW name of the simulation: ")

simulation_filepath_new = "{0}/{1}".format(simulation_base_filepath, simulation_name_new)



os.system("mv {0} {1}".format(simulation_filepath_old, simulation_filepath_new))

old_files = glob.glob("{0}/output/*.hdf5".format(simulation_filepath_new))

for file in old_files:
	numeric_id_start = 0
	for i in range (1, len(file)):
		if file[-i] == "_":
			numeric_id_start = i
			break

	new_filepath = file[:len("{0}/output/".format(simulation_filepath_new))] + simulation_name_new + file[-numeric_id_start:]
	os.system("mv {0} {1}".format(file, new_filepath))
	
os.system("mv {0}/output/{1}.xmf {0}/output/{2}.xmf".format(simulation_filepath_new, simulation_name_old, simulation_name_new))

os.system("mv {0}/output/ {0}/RENAMED_output".format(simulation_filepath_new))

os.system("mv {0}/{1}.hdf5 {0}/{2}.hdf5".format(simulation_filepath_new, simulation_name_old, simulation_name_new))

os.system("mv {0}/{1}.yml {0}/{2}.yml".format(simulation_filepath_new, simulation_name_old, simulation_name_new))



visualised_filepath_old = "{0}/{1}".format(visualised_base_filepath, simulation_name_old)
visualised_filepath_new = "{0}/{1}".format(visualised_base_filepath, simulation_name_new)


os.system("mv {0} {1}".format(visualised_filepath_old, visualised_filepath_new))


old_files = glob.glob("{0}/*.png".format(visualised_filepath_new))

for file in old_files:
	numeric_id_start = 0
	for i in range (1, len(file)):
		if file[-i] == "_":
			numeric_id_start = i
			break

	new_filepath = file[:len("{0}/".format(visualised_filepath_new))] + simulation_name_new + file[-numeric_id_start:]
	os.system("mv {0} {1}".format(file, new_filepath))

#os.system("mv {0}/{1}.mp4 {0}/{2}.mp4".format(visualised_filepath_new, simulation_name_old, simulation_name_new))



