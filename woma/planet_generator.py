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

import woma
import h5py
import os

import womaplotting

R_earth = 6.371e6   # m
M_earth = 5.9722e24  # kg
G = 6.67430e-11  # m^3 kg^-1 s^-2

## Define the planet
planet = woma.Planet( 
    name            = "3 Layer Uranus v2 For 0.875M Impactor", 
    A1_mat_layer    = ["ANEOS_forsterite", "AQUA", "HM80_HHe"], 
    A1_T_rho_type   = ["entropy=4040", "adiabatic", "adiabatic"], 
    P_s             = 1e5, 
    T_s             = 60, 
    M               = 13.665 * M_earth, 
    A1_R_layer      = [None, None, 3.98 * R_earth], 
    I_MR2           = 0.180
)
## Converge on a solution with these planet parameters
planet.gen_prof_L3_find_R1_R2_given_M_R_I(R_1_min=0.85*R_earth, R_1_max=1.15*R_earth)


output_directory = "planetesimal_files/{0}/".format(planet.name.replace(" ", "_"))

if os.path.exists(output_directory) == False:
	os.makedirs(output_directory)

## Plot profiles for sanity checking
womaplotting.plot_profiles(planet, output_directory)

resolution_input = input("Particle resolution: ")

if resolution_input != "":
	resolution = int(resolution_input)
else:
	resolution = 1e6

## Place particles, at the required resolution, onto the planet model
particles = woma.ParticlePlanet(planet, resolution, verbosity=0)
womaplotting.plot_particles(particles, planet, "{0}-cross-section-{1:.0e}".format(planet.name.replace(" ", "-"), resolution), output_directory)

filename = "{0}{1}.hdf5".format(output_directory, input("Name of particle file: "))

## Save the particle configuration for this planet
with h5py.File(filename, "w") as f:
	woma.save_particle_data(
	f,
	particles.A2_pos,
	particles.A2_vel,
	particles.A1_m,
        particles.A1_h,
        particles.A1_rho,
        particles.A1_P,
        particles.A1_u,
        particles.A1_mat_id,
	A1_s=particles.A1_u,
	boxsize=15 * R_earth
	)
print("Done!")


