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

import matplotlib.pyplot as plt
import numpy as np
import glob
import sys
import os
import math

from PIL import Image



##
##
## Get the name of the simulation
if (len(sys.argv) > 1):
	simulation_name = sys.argv[1]
else:
	simulation_name = input("Enter the name of the simulation: ")




for folder in ['xy', 'yz', 'xz']:
	files = glob.glob("simulations/{0}/{1}/*.png".format(simulation_name, folder))
	files.sort()
	for image_path in files:
		single_image = Image.open(image_path)

		new_image = Image.new('RGB',(single_image.size[0] * 2, single_image.size[1]), (0, 0, 0))

		new_image.paste(single_image, (single_image.size[0] // 2, 0))
		filename = "{0}wide_{1}".format(image_path[:-9], image_path[-9:])
		new_image.save(filename)
		#error = error / 0
		sys.stdout.write("\rSaved {0}!".format(filename))
		sys.stdout.flush()