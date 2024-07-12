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

import swiftsimio as sw
import numpy as np
import unyt

from custom_functions import material_colour_map


def load_to_woma(snapshot, num_target_particles=-1):
	snapshot_data = sw.load(snapshot)
	box_mid = 0.5 * snapshot_data.metadata.boxsize[0].to(unyt.m)
	snapshot_data.gas.coordinates.convert_to_mks()
	pos = np.array(snapshot_data.gas.coordinates - box_mid)
	snapshot_data.gas.velocities.convert_to_mks()
	vel = np.array(snapshot_data.gas.velocities)
	snapshot_data.gas.smoothing_lengths.convert_to_mks()
	h = np.array(snapshot_data.gas.smoothing_lengths)
	snapshot_data.gas.masses.convert_to_mks()
	m = np.array(snapshot_data.gas.masses)
	snapshot_data.gas.densities.convert_to_mks()
	rho = np.array(snapshot_data.gas.densities)
	snapshot_data.gas.pressures.convert_to_mks()
	p = np.array(snapshot_data.gas.pressures)
	snapshot_data.gas.internal_energies.convert_to_mks()
	u = np.array(snapshot_data.gas.internal_energies)
	mat_id = np.array(snapshot_data.gas.material_ids)
	id = np.array(snapshot_data.gas.particle_ids)
    
	pos_centerM = np.sum(pos * m[:, np.newaxis], axis=0) / np.sum(m)
	vel_centerM = np.sum(vel * m[:, np.newaxis], axis=0) / np.sum(m)

	pos -= pos_centerM
	vel -= vel_centerM

	xy = np.hypot(pos[:, 0], pos[:, 1])
	r = np.hypot(xy, pos[:, 2])
	r = np.sort(r)
	R = np.mean(r[-1000:])

	if num_target_particles != -1:
		# Edit material IDs for particles in the impactor
		mat_id[num_target_particles <= id] += material_colour_map.id_body

	return pos, vel, h, m, rho, p, u, mat_id, R

def bound_load_to_woma(snapshot, remnant_id):
	pos, vel, h, m, rho, p, u, mat_id, R = load_to_woma(snapshot)
	
	snapshot_data = sw.load(snapshot)
	bound_id = np.array(snapshot_data.gas.bound_ids, dtype=np.int32)
	mask = bound_id == remnant_id
	
	return pos[mask], vel[mask], h[mask], m[mask], rho[mask], p[mask], u[mask], mat_id[mask], R
	
	

