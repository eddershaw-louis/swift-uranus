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

planets = []
impactors = []

planets.append(woma.Planet( 
    name            = "Uranus", 
    A1_mat_layer    = ["ANEOS_forsterite", "AQUA", "HM80_HHe"], 
    A1_T_rho_type   = ["entropy=4047", "adiabatic", "adiabatic"], 
    P_s             = 1e5, 
    T_s             = 60, 
    M               = 14.54 * M_earth, 
    A1_R_layer      = [None, None, 3.98 * R_earth], 
    I_MR2           = 0.184
))
planets[-1].gen_prof_L3_find_R1_R2_given_M_R_I(R_1_min=0.9*R_earth, R_1_max=1.1*R_earth)

#planets.append(woma.Planet( 
#    name            = r"Uranus -0.5M$_\oplus$", 
#    A1_mat_layer    = ["ANEOS_forsterite", "AQUA", "HM80_HHe"], 
#    A1_T_rho_type   = ["entropy=4040", "adiabatic", "adiabatic"], 
#    P_s             = 1e5, 
#    T_s             = 60, 
#    M               = 14.04 * M_earth, 
#    A1_R_layer      = [None, None, 3.98 * R_earth], 
#    I_MR2           = 0.181
#))
#planets[-1].gen_prof_L3_find_R1_R2_given_M_R_I(R_1_min=0.9*R_earth, R_1_max=1.1*R_earth)


#output_path = "multiple_planets.png"
#womaplotting.plot_multiple_profiles(planets, impactors, output_path)

#planets.append(woma.Planet( 
#    name            = r"Uranus -0.6M$_\oplus$", 
#    A1_mat_layer    = ["ANEOS_forsterite", "AQUA", "HM80_HHe"], 
#    A1_T_rho_type   = ["entropy=4040", "adiabatic", "adiabatic"], 
#    P_s             = 1e5, 
#    T_s             = 60, 
#    M               = 13.94 * M_earth, 
#    A1_R_layer      = [None, None, 3.98 * R_earth], 
#    I_MR2           = 0.184
#))
#planets[-1].gen_prof_L3_find_R1_R2_given_M_R_I(R_1_min=0.85*R_earth, R_1_max=1*R_earth)

planets.append(woma.Planet( 
    name            = r"Ur. 0.7",#M$_\oplus$", 
    A1_mat_layer    = ["ANEOS_forsterite", "AQUA", "HM80_HHe"], 
    A1_T_rho_type   = ["entropy=4040", "adiabatic", "adiabatic"], 
    P_s             = 1e5, 
    T_s             = 60, 
    M               = 13.84 * M_earth, 
    A1_R_layer      = [None, None, 3.98 * R_earth], 
    I_MR2           = 0.184
))
planets[-1].gen_prof_L3_find_R1_R2_given_M_R_I(R_1_min=0.85*R_earth, R_1_max=1*R_earth)

#output_path = "multiple_planets.png"
#womaplotting.plot_multiple_profiles(planets, impactors, output_path)
#quit()

#planets.append(woma.Planet( 
#    name            = r"Uranus -0.75M$_\oplus$", 
#    A1_mat_layer    = ["ANEOS_forsterite", "AQUA", "HM80_HHe"], 
#    A1_T_rho_type   = ["entropy=4040", "adiabatic", "adiabatic"], 
#    P_s             = 1e5, 
#    T_s             = 60, 
#    M               = 13.79 * M_earth, 
#    A1_R_layer      = [None, None, 3.98 * R_earth], 
#    I_MR2           = 0.184
#))
#planets[-1].gen_prof_L3_find_R1_R2_given_M_R_I(R_1_min=0.85*R_earth, R_1_max=1*R_earth)

planets.append(woma.Planet( 
    name            = r"Ur. 1",#M$_\oplus$", 
    A1_mat_layer    = ["ANEOS_forsterite", "AQUA", "HM80_HHe"], 
    A1_T_rho_type   = ["entropy=4040", "adiabatic", "adiabatic"], 
    P_s             = 1e5, 
    T_s             = 60, 
    M               = 13.54 * M_earth, 
    A1_R_layer      = [None, None, 3.98 * R_earth], 
    I_MR2           = 0.179
))
planets[-1].gen_prof_L3_find_R1_R2_given_M_R_I(R_1_min=0.9*R_earth, R_1_max=1.1*R_earth)

planets.append(woma.Planet( 
    name            = r"Ur. 1.125", 
    A1_mat_layer    = ["ANEOS_forsterite", "AQUA", "HM80_HHe"], 
    A1_T_rho_type   = ["entropy=4040", "adiabatic", "adiabatic"], 
    P_s             = 1e5, 
    T_s             = 60, 
    M               = 13.415 * M_earth, 
    A1_R_layer      = [None, None, 3.98 * R_earth], 
    I_MR2           = 0.182
))
planets[-1].gen_prof_L3_find_R1_R2_given_M_R_I(R_1_min=0.8*R_earth, R_1_max=1*R_earth)

#planets.append(woma.Planet( 
#    name            = r"Ur. -1.25",#M$_\oplus$", 
#    A1_mat_layer    = ["ANEOS_forsterite", "AQUA", "HM80_HHe"], 
#    A1_T_rho_type   = ["entropy=4040", "adiabatic", "adiabatic"], 
#    P_s             = 1e5, 
#    T_s             = 60, 
#    M               = 13.29 * M_earth, 
#    A1_R_layer      = [None, None, 3.98 * R_earth], 
#    I_MR2           = 0.182
#))
#planets[-1].gen_prof_L3_find_R1_R2_given_M_R_I(R_1_min=0.8*R_earth, R_1_max=1*R_earth)

#planets.append(woma.Planet( 
#    name            = r"Uranus -1.5M$_\oplus$", 
#    A1_mat_layer    = ["ANEOS_forsterite", "AQUA", "HM80_HHe"], 
#    A1_T_rho_type   = ["entropy=4040", "adiabatic", "adiabatic"], 
#    P_s             = 1e5, 
#    T_s             = 60, 
#    M               = 13.04 * M_earth, 
#    A1_R_layer      = [None, None, 3.98 * R_earth], 
#    I_MR2           = 0.181
#))
#planets[-1].gen_prof_L3_find_R1_R2_given_M_R_I(R_1_min=0.8*R_earth, R_1_max=1*R_earth)

#planets.append(woma.Planet( 
#    name            = r"Uranus -1.75M$_\oplus$", 
#    A1_mat_layer    = ["ANEOS_forsterite", "AQUA", "HM80_HHe"], 
#    A1_T_rho_type   = ["entropy=4040", "adiabatic", "adiabatic"], 
#    P_s             = 1e5, 
#    T_s             = 60, 
#    M               = 12.79 * M_earth, 
#    A1_R_layer      = [None, None, 3.98 * R_earth], 
#    I_MR2           = 0.181
#))
#planets[-1].gen_prof_L3_find_R1_R2_given_M_R_I(R_1_min=0.8*R_earth, R_1_max=1*R_earth)



#impactors.append(woma.Planet( 
#    name            = r"Imp. 0.5M$_\oplus$", 
#    A1_mat_layer    = ["ANEOS_forsterite", "AQUA"], 
#    A1_T_rho_type   = ["entropy=1400", "adiabatic"], 
#    P_s             = 1e9, 
#    T_s             = 550, 
#    A1_M_layer      = [0.08645 * M_earth, 0.41355 * M_earth]
#))
#impactors[-1].gen_prof_L2_find_R_R1_given_M1_M2(R_min=1*R_earth, R_max=1.2*R_earth)

#impactors.append(woma.Planet( 
#    name            = r"Imp. 0.6M$_\oplus$", 
#    A1_mat_layer    = ["ANEOS_forsterite", "AQUA"], 
#    A1_T_rho_type   = ["entropy=1540", "adiabatic"], 
#    P_s             = 1e9, 
#    T_s             = 550, 
#    A1_M_layer      = [0.10374 * M_earth, 0.49626 * M_earth]
#))
#impactors[-1].gen_prof_L2_find_R_R1_given_M1_M2(R_min=1.15*R_earth, R_max=1.225*R_earth)

impactors.append(woma.Planet( 
    name            = r"Im. 0.7",#M$_\oplus$", 
    A1_mat_layer    = ["ANEOS_forsterite", "AQUA"], 
    A1_T_rho_type   = ["entropy=1620", "adiabatic"], 
    P_s             = 1e9, 
    T_s             = 550, 
    A1_M_layer      = [0.12103 * M_earth, 0.57897 * M_earth]
))
impactors[-1].gen_prof_L2_find_R_R1_given_M1_M2(R_min=1.2*R_earth, R_max=1.3*R_earth)

#impactors.append(woma.Planet( 
#    name            = r"Imp. 0.75M$_\oplus$", 
#    A1_mat_layer    = ["ANEOS_forsterite", "AQUA"], 
#    A1_T_rho_type   = ["entropy=1400", "adiabatic"], 
#    P_s             = 1e9, 
#    T_s             = 550, 
#    A1_M_layer      = [0.129675 * M_earth, 0.620325 * M_earth]
#))
#impactors[-1].gen_prof_L2_find_R_R1_given_M1_M2(R_min=1.2*R_earth, R_max=1.32*R_earth)

impactors.append(woma.Planet( 
    name            = r"Im. 1",#M$_\oplus$", 
    A1_mat_layer    = ["ANEOS_forsterite", "AQUA"], 
    A1_T_rho_type   = ["entropy=1850", "adiabatic"], 
    P_s             = 1e9, 
    T_s             = 550, 
    A1_M_layer      = [0.1729 * M_earth, 0.8271 * M_earth]
))
impactors[-1].gen_prof_L2_find_R_R1_given_M1_M2(R_min=1.2*R_earth, R_max=1.45*R_earth)

impactors.append(woma.Planet( 
    name            = r"Im. 1.125", 
    A1_mat_layer    = ["ANEOS_forsterite", "AQUA"], 
    A1_T_rho_type   = ["entropy=1980", "adiabatic"], 
    P_s             = 1e9, 
    T_s             = 550, 
    A1_M_layer      = [0.1945125 * M_earth, 0.9304875 * M_earth]
))
impactors[-1].gen_prof_L2_find_R_R1_given_M1_M2(R_min=1.3*R_earth, R_max=1.5*R_earth)

#impactors.append(woma.Planet( 
#    name            = r"Im. 1.25",#M$_\oplus$", 
#    A1_mat_layer    = ["ANEOS_forsterite", "AQUA"], 
#    A1_T_rho_type   = ["entropy=2100", "adiabatic"], 
#    P_s             = 1e9, 
#    T_s             = 550, 
#    A1_M_layer      = [0.216125 * M_earth, 1.033875 * M_earth]
#))
#impactors[-1].gen_prof_L2_find_R_R1_given_M1_M2(R_min=1.3*R_earth, R_max=1.5*R_earth)

#impactors.append(woma.Planet( 
#    name            = r"Imp. 1.5M$_\oplus$", 
#    A1_mat_layer    = ["ANEOS_forsterite", "AQUA"], 
#    A1_T_rho_type   = ["entropy=2470", "adiabatic"], 
#    P_s             = 1e9, 
#    T_s             = 550, 
#    A1_M_layer      = [0.25935 * M_earth, 1.24065 * M_earth]
#))
#impactors[-1].gen_prof_L2_find_R_R1_given_M1_M2(R_min=1.3*R_earth, R_max=1.6*R_earth)

#impactors.append(woma.Planet( 
#    name            = r"Imp. 1.75M$_\oplus$", 
#    A1_mat_layer    = ["ANEOS_forsterite", "AQUA"], 
#    A1_T_rho_type   = ["entropy=2480", "adiabatic"], 
#    P_s             = 1e9, 
#    T_s             = 550, 
#    A1_M_layer      = [0.302575 * M_earth, 1.447425 * M_earth]
#))
#impactors[-1].gen_prof_L2_find_R_R1_given_M1_M2(R_min=1.35*R_earth, R_max=1.65*R_earth)


################################ ELSA ###############################################
# Create planet
#planets.append(woma.Planet(
#    name            = "Uranus",
#    A1_mat_layer    = ["ANEOS_forsterite", "AQUA", "HM80_HHe"],
#    A1_T_rho_type   = ["entropy=4000", "adiabatic", "adiabatic"],            
#    M               = 14.54 * M_earth,
#    A1_R_layer      = [None, None, 3.98 * R_earth],
#    I_MR2           = 0.183,                             
#    P_s             = 1e5,
#    T_s             = 60,
#))
# Generate the profiles
#planets[-1].gen_prof_L3_find_R1_R2_given_M_R_I(R_1_min=0.90*R_earth, R_1_max=1.10*R_earth)

#planets.append()
#planets[-1].


# Generating Impactor
#impactors.append(woma.Planet( 
#    name            = "Rock Imp. 0.2M", 
#    A1_mat_layer    = ["ANEOS_forsterite"],
#    A1_T_rho_type   = ["entropy=2600"],       
#    P_s             = 1e9, 
#    T_s             = 450, 
#    M               = 0.2 * M_earth,
#))
# Generate the profiles 
#impactors[-1].gen_prof_L1_find_R_given_M(R_max=0.7 * R_earth)

# Generating Impactor
#impactors.append(woma.Planet( 
#    name            = "Rock Imp. 0.8M", 
#    A1_mat_layer    = ["ANEOS_forsterite"],
#    A1_T_rho_type   = ["entropy=2600"],       
#    P_s             = 1e9, 
#    T_s             = 450, 
#    M               = 0.8 * M_earth,
#))
# Generate the profiles 
#impactors[-1].gen_prof_L1_find_R_given_M(R_max=1.30 * R_earth)

output_path = "Planetary_Profiles.png"
womaplotting.plot_multiple_profiles(planets, impactors, output_path)