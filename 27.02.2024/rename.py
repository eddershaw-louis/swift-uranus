## Rename
import sys
import os
import glob

def rename_images(files, view):
	for file in files:
		numeric_id_start = 0
		for i in range (1, len(file)):
			if file[-i] == "_":
				numeric_id_start = i
				break
	
		new_filepath = file[:len("{0}/{1}/".format(visualised_filepath_new, view))] + simulation_name_new + file[-numeric_id_start:]
		os.system("mv {0} {1}".format(file, new_filepath))


## Filepath to the SWIFT simulation directory and the output image directory
simulation_base_filepath = "/data/cluster4/hd20558/simulations"
visualised_base_filepath = "/home/hd20558/files/simulations"
#
#
## Get the name of the simulation the user wants to rename
if (len(sys.argv) > 1):
	simulation_name_old = sys.argv[1]
else:
	simulation_name_old = input("Enter the name of the simulation to rename: ")

simulation_filepath_old = "{0}/{1}".format(simulation_base_filepath, simulation_name_old)
#
#
#
if ('-a' in sys.argv):
	simulation_name_new = sys.argv[sys.argv.index('-a') + 1] + "_" + simulation_name_old
else:
	simulation_name_new = False
print(simulation_name_new)
#
#
## Get the new name that they want the previous simulation to now have
if (len(sys.argv) > 2 and simulation_name_new == False):
	simulation_name_new = sys.argv[2]
elif simulation_name_new == False:
	simulation_name_new = input("Enter the NEW name of the simulation: ")

simulation_filepath_new = "{0}/{1}".format(simulation_base_filepath, simulation_name_new)


## Rename the directory in the scratch space to the new name
os.system("mv {0} {1}".format(simulation_filepath_old, simulation_filepath_new))

## Get all of the output hdf5 files in the directory (which has now been renamed to the new one)
old_files = glob.glob("{0}/output/*.hdf5".format(simulation_filepath_new))

## Go through all of the hdf5 files and rename them to have the new simulation name
for file in old_files:
	numeric_id_start = 0
	
	## We need to find the number of this hdf5 output, which will be listed just after the last "_" in the filename
	for i in range (1, len(file)):
		if file[-i] == "_":
			numeric_id_start = i
			break

	## Rename this file to have the new simulation name before its numerical index
	new_filepath = file[:len("{0}/output/".format(simulation_filepath_new))] + simulation_name_new + file[-numeric_id_start:]
	os.system("mv {0} {1}".format(file, new_filepath))

## Rename the xmf file in the output directory
os.system("mv {0}/output/{1}.xmf {0}/output/{2}.xmf".format(simulation_filepath_new, simulation_name_old, simulation_name_new))

## Rename the output directory
## This acts as a record that the simulation has been renamed, and thus the .yml file might be pointing to old filenames inside it.
## If the user sees RENAMED_output then they should double check the .yml file and then rename the output directory to just "output" which then 'completes' the rename
#os.system("mv {0}/output/ {0}/RENAMED_output".format(simulation_filepath_new))

## Rename the initial hdf5 file for this simulation
os.system("mv {0}/{1}.hdf5 {0}/{2}.hdf5".format(simulation_filepath_new, simulation_name_old, simulation_name_new))

## Rename the parameter file for this simulation
os.system("mv {0}/{1}.yml {0}/{2}.yml".format(simulation_filepath_new, simulation_name_old, simulation_name_new))


## Get the old and new filepaths to the (to be) renamed images
visualised_filepath_old = "{0}/{1}".format(visualised_base_filepath, simulation_name_old)
visualised_filepath_new = "{0}/{1}".format(visualised_base_filepath, simulation_name_new)

## Rename the simulation images directory to the new name 
os.system("mv {0} {1}".format(visualised_filepath_old, visualised_filepath_new))

## Rename all the xy images for this simulation
old_image_files = glob.glob("{0}/xy/*.png".format(visualised_filepath_new))
rename_images(old_image_files, "xy")

## Rename all the xz images for this simulation
old_image_files = glob.glob("{0}/xz/*.png".format(visualised_filepath_new))
rename_images(old_image_files, "xz")

## Rename all the yz images for this simulation
old_image_files = glob.glob("{0}/yz/*.png".format(visualised_filepath_new))
rename_images(old_image_files, "yz")

## Rename all the combined xy-xz images for this simulation
old_image_files = glob.glob("{0}/xy_xz/*.png".format(visualised_filepath_new))
rename_images(old_image_files, "xy_xz")

## Rename all the combined xy-yz images for this simulation
old_image_files = glob.glob("{0}/xy_yz/*.png".format(visualised_filepath_new))
rename_images(old_image_files, "xy_yz")

## Rename all the combined xy-xz-yz images for this simulation
old_image_files = glob.glob("{0}/xy_xz_yz/*.png".format(visualised_filepath_new))
rename_images(old_image_files, "xy_xz_yz")