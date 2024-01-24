from planetboundmass import Bound
import matplotlib.pyplot as plt

def main(args):
	filename = args[1]

	if ('-n' in args):
		npt = int(args[args.index('-n') + 1])
	else:
		npt = int(input("Initial number of particles in target: "))

	if ('-m' in args):
		total_mass = float(args[args.index('-m') + 1])
	else:
		total_mass = float(input("Total mass of the system (M_earth): "))

	if ('-r' in args):
		num_rem = int(args[args.index('-r') + 1])
	else:
		num_rem = int(input("Expected number of remnants: "))
	

	bound = Bound(filename, verbose=1, npt=npt, total_mass=total_mass, num_rem=num_rem)
	bound.find_bound()
	bound.write_bound_id()
	
	if ('-plot' in args):
		bound.basic_plot(mode=-1, equal_axis=True)