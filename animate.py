import os
import sys

if (len(sys.argv) > 1):
        simulation_name = sys.argv[1]
else:
        simulation_name = input("Enter the name of the simulation: ")

if (len(sys.argv) > 2):
	framerate = sys.argv[2]
else:
	framerate_input = input("Video framerate: ")
	if framerate_input == "":
		framerate = 24
	else:
		framerate = framerate_input

os.system("ffmpeg -framerate {1} -pattern_type glob -i 'simulations/{0}/*.png' -c:v libx264 simulations/{0}/animation.mp4".format(simulation_name, framerate))

quit()

if (input("Keep frames? (y): ").lower() == "n"):
	os.system("rm -f simulations/{0}/*.png".format(simulation_name))
