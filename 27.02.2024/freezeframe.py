import os
import sys
import glob


if (len(sys.argv) > 1):
	simulation_name = sys.argv[1]

if ('-s' in sys.argv):
	ff_start = True
	ff_start_duration = int(sys.argv[sys.argv.index('-s') + 1])
else:
	ff_start = False

if ('-e' in sys.argv):
	ff_end = True
	ff_end_duration = int(sys.argv[sys.argv.index('-e') + 1])
else:
	ff_end = False

if ('-r' in sys.argv):
	ff_remove = True
else:
	ff_remove = False

if ff_remove:
	for folder in ["xy", "xz", "yz", "xy_xz", "xy_yz", "xy_xz_yz"]:
		ff_files = glob.glob("{0}/{1}/*_ff_*.png".format(simulation_name, folder))
		if len(ff_files) > 0:
			os.system("rm {0}/{1}/*_ff_*.png".format(simulation_name, folder))


if ff_start:
	for folder in ["xy", "xz", "yz", "xy_xz", "xy_yz", "xy_xz_yz"]:
		ff_files = glob.glob("{0}/{1}/*_ff_s*.png".format(simulation_name, folder))
		if len(ff_files) > 0:
			os.system("rm {0}/{1}/*_ff_s*.png".format(simulation_name, folder))

		files = glob.glob("{0}/{1}/*[!_ff_s]*.png".format(simulation_name, folder))
		if len(files) > 0:
			files.sort()
			#print(files)
			frame = files[0]		
		
		for i in range(ff_start_duration - 1):
			os.system("cp {0} {1}0_ff_s_{2}.png".format(frame, frame[:-4], i + 1))

if ff_end:
	for folder in ["xy_xz_yz"]: #["xy", "xz", "yz", "xy_xz", "xy_yz", "xy_xz_yz"]:
		ff_files = glob.glob("{0}/{1}/*_ff_e*.png".format(simulation_name, folder))
		if len(ff_files) > 0:
			os.system("rm {0}/{1}/*_ff_e*.png".format(simulation_name, folder))

		files = glob.glob("{0}/{1}/*[!_ff_e]*.png".format(simulation_name, folder))
		if len(files) > 0:
			files.sort()
			#print(files)
			frame = files[-1]		
		
		for i in range(ff_end_duration - 1):
			os.system("cp {0} {1}_ff_e_{2}.png".format(frame, frame[:-4], i + 1))

