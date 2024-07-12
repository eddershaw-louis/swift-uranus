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

import os
import sys
import glob

## Get the name of the simulation to combine its images into a video
if (len(sys.argv) > 1):
        simulation_name = sys.argv[1]
else:
        simulation_name = input("Enter the name of the simulation: ")
#
#
## Get the desired framerate from the user
if (len(sys.argv) > 2):
	framerate = sys.argv[2]
else:
	framerate_input = input("Video framerate: ")
	if framerate_input == "":
		framerate = 24
	else:
		framerate = framerate_input

## Generate a video of the xy images for this simulation, if they exist
if (len(glob.glob('simulations/{0}/xy/*.png'.format(simulation_name)))) > 0:
	os.system("ffmpeg -framerate {1} -pattern_type glob -i 'simulations/{0}/xy/*.png' -c:v libx264 -pix_fmt yuv420p simulations/{0}/xy_animation.mp4".format(simulation_name, framerate))
	pass

## Generate a video of the xz images for this simulation, if they exist
if (len(glob.glob('simulations/{0}/xz/*.png'.format(simulation_name)))) > 0:
	#os.system("ffmpeg -framerate {1} -pattern_type glob -i 'simulations/{0}/xz/*.png' -c:v libx264 -pix_fmt yuv420p simulations/{0}/xz_animation.mp4".format(simulation_name, framerate))
	pass

## Generate a video of the yz images for this simulation, if they exist
if (len(glob.glob('simulations/{0}/yz/*.png'.format(simulation_name)))) > 0:
	#os.system("ffmpeg -framerate {1} -pattern_type glob -i 'simulations/{0}/yz/*.png' -c:v libx264 -pix_fmt yuv420p simulations/{0}/yz_animation.mp4".format(simulation_name, framerate))
	pass

## Generate a video of the xy-xz images for this simulation, if they exist
if (len(glob.glob('simulations/{0}/xy_xz/*.png'.format(simulation_name)))) > 0:
	#os.system("ffmpeg -framerate {1} -pattern_type glob -i 'simulations/{0}/xy_xz/*.png' -c:v libx264 -pix_fmt yuv420p simulations/{0}/xy_xz_animation.mp4".format(simulation_name, framerate))
	pass

## Generate a video of the xy-yz images for this simulation, if they exist
if (len(glob.glob('simulations/{0}/xy_yz/*.png'.format(simulation_name)))) > 0:
	os.system("ffmpeg -framerate {1} -pattern_type glob -i 'simulations/{0}/xy_yz/*.png' -c:v libx264 -pix_fmt yuv420p -crf 20 simulations/{0}/xy_yz_animation.mp4".format(simulation_name, framerate))
	pass

## Generate a video of the xz-xz-yz images for this simulation, if they exist
if (len(glob.glob('simulations/{0}/xy_xz_yz/*.png'.format(simulation_name)))) > 0:
	os.system("ffmpeg -framerate {1} -pattern_type glob -i 'simulations/{0}/xy_xz_yz/*.png' -c:v libx264 -pix_fmt yuv420p simulations/{0}/xy_xz_yz_animation.mp4".format(simulation_name, framerate))
	pass

## Don't ask the user if they want to keep the frames
## The images don't take up that much room and are good for reference
quit()

## Ask the user if they want to delete all the frames now that they have been combined into a video, in order to save disk space if necessary
if (input("Keep frames? (y): ").lower() == "n"):
	os.system("rm -f simulations/{0}/*.png".format(simulation_name))
