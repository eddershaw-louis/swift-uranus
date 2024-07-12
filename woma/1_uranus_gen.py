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
import matplotlib.pyplot as plt
import h5py

R_earth = 6.371e6   # m
M_earth = 5.9724e24  # kg

def plot_spherical_profiles(planet):
    fig, ax = plt.subplots(2, 2, figsize=(8,8))

    ax[0, 0].plot(planet.A1_r / R_earth, planet.A1_rho)
    ax[0, 0].set_xlabel(r"Radius, $r$ $[R_\oplus]$")
    ax[0, 0].set_ylabel(r"Density, $\rho$ [kg m$^{-3}$]")
    ax[0, 0].set_yscale("log")
    ax[0, 0].set_xlim(0, None)

    ax[1, 0].plot(planet.A1_r / R_earth, planet.A1_m_enc / M_earth)
    ax[1, 0].set_xlabel(r"Radius, $r$ $[R_\oplus]$")
    ax[1, 0].set_ylabel(r"Enclosed Mass, $M_{<r}$ $[M_\oplus]$")
    ax[1, 0].set_xlim(0, None)
    ax[1, 0].set_ylim(0, None)

    ax[0, 1].plot(planet.A1_r / R_earth, planet.A1_P)
    ax[0, 1].set_xlabel(r"Radius, $r$ $[R_\oplus]$")
    ax[0, 1].set_ylabel(r"Pressure, $P$ [Pa]")
    ax[0, 1].set_yscale("log")
    ax[0, 1].set_xlim(0, None)

    ax[1, 1].plot(planet.A1_r / R_earth, planet.A1_T)
    ax[1, 1].set_xlabel(r"Radius, $r$ $[R_\oplus]$")
    ax[1, 1].set_ylabel(r"Temperature, $T$ [K]")
    ax[1, 1].set_xlim(0, None)
    ax[1, 1].set_ylim(0, None)

    plt.tight_layout()
    #plt.show()
    plt.savefig("{0}.png".format(planet.name.replace(" ", "-")))
    plt.close()

def plot_particles(particles, planet, filename):
    materials = list(set(particles.A1_mat_id))
    
    fig, ax = plt.subplots(1, 1, figsize=(5,5))
    
    for material in materials:
        material_indexes = [i for i in range(len(particles.A2_pos)) if particles.A1_mat_id[i] == material]
        material_pos_xs = []
        material_pos_ys = []
        for index in material_indexes:
            slice_percentage = 0.01
            if particles.A2_pos[index][2] < planet.R * slice_percentage and particles.A2_pos[index][2] > - planet.R * slice_percentage:
                material_pos_xs += [particles.A2_pos[index][0]/R_earth]
                material_pos_ys += [particles.A2_pos[index][1]/R_earth]
                
        ax.scatter(material_pos_xs, material_pos_ys, label=planet.A1_mat_layer[planet.A1_mat_id_layer.index(material)])
    
    axis_lim = planet.R * 1.05 / R_earth
    ax.set_xlim(-axis_lim, axis_lim)
    ax.set_xlabel(r"x, $[R_\oplus]$")
    ax.set_ylim(-axis_lim, axis_lim)
    ax.set_ylabel(r"y, $[R_\oplus]$")
    ax.set_aspect('equal')
    ax.legend()
    
    plt.tight_layout()
    #plt.show()
    plt.savefig("{0}.png".format(filename))
    plt.close()

    """
    fig = plt.figure(figsize=plt.figaspect(1))
    ax = fig.add_subplot(projection='3d')
    
    material_pos_xs_3D = []
    material_pos_ys_3D = []
    material_pos_zs_3D = []
    for material in materials:
        material_indexes = [i for i in range(len(particles.A2_pos)) if particles.A1_mat_id[i] == material]

        
        for index in material_indexes:
            if particles.A2_pos[index][2] > 0:
                material_pos_xs_3D += [particles.A2_pos[index][0]/R_earth]
                material_pos_ys_3D += [particles.A2_pos[index][1]/R_earth]
                material_pos_zs_3D += [particles.A2_pos[index][2]/R_earth]
        #fig = plt.figure(figsize=plt.figaspect(1))
        #ax = fig.add_subplot(projection='3d')
        ax.plot_surface(material_pos_xs_3D, material_pos_zs_3D, material_pos_ys_3D)
        #plt.savefig("{0}-3D-cross-section-{1}.png".format(planet.name.replace(" ", "-"), material))
        #plt.close()
    #plt.savefig("{0}-3D-cross-section.png".format(planet.name.replace(" ", "-")))
    plt.show()
    plt.close()
    """

planet = woma.Planet(
    name            = "3 Layer Uranus v1.0",
    A1_mat_layer    = ["HM80_rock", "HM80_ice", "HM80_HHe"],
    A1_T_rho_type   = ["power=0", "power=0.9", "adiabatic"],
    P_s             = 1e5,
    T_s             = 70,
    M               = 14.5 * M_earth,
    A1_R_layer      = [None, 3 * R_earth, 4 * R_earth],
)

planet.gen_prof_L3_find_R1_given_M_R_R2()

plot_spherical_profiles(planet)


#resolution = 1e5
#particles_medium_res = woma.ParticlePlanet(planet, resolution, verbosity=0)
#plot_particles(particles_medium_res, planet, "{0}-cross-section-{1:.0e}".format(planet.name.replace(" ", "-"), resolution))

resolution = 1e6
particles_high_res = woma.ParticlePlanet(planet, resolution, verbosity=0)
plot_particles(particles_high_res, planet, "{0}-cross-section-{1:.0e}".format(planet.name.replace(" ", "-"), resolution))

filename = "uranusV1.hdf5"
particles_high_res.save(filename)

particles = particles_high_res

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
	boxsize=15 * R_earth
	)
print("Done!")
