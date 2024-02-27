import swiftsimio as sw
import numpy as np
import unyt

def load_to_woma(snapshot):
	# Load
	data = sw.load(snapshot)
	box_mid = 0.5 * data.metadata.boxsize[0].to(unyt.m)
	data.gas.coordinates.convert_to_mks()
	pos = np.array(data.gas.coordinates - box_mid)
	data.gas.velocities.convert_to_mks()
	vel = np.array(data.gas.velocities)
	data.gas.smoothing_lengths.convert_to_mks()
	h = np.array(data.gas.smoothing_lengths)
	data.gas.masses.convert_to_mks()
	m = np.array(data.gas.masses)
	data.gas.densities.convert_to_mks()
	rho = np.array(data.gas.densities)
	data.gas.pressures.convert_to_mks()
	p = np.array(data.gas.pressures)
	data.gas.internal_energies.convert_to_mks()
	u = np.array(data.gas.internal_energies)
	matid = np.array(data.gas.material_ids)
	# pid     = np.array(data.gas.particle_ids)
    
	pos_centerM = np.sum(pos * m[:, np.newaxis], axis=0) / np.sum(m)
	vel_centerM = np.sum(vel * m[:, np.newaxis], axis=0) / np.sum(m)

	pos -= pos_centerM
	vel -= vel_centerM

	pos_noatmo = pos[matid != 200]

	xy = np.hypot(pos_noatmo[:, 0], pos_noatmo[:, 1])
	r = np.hypot(xy, pos_noatmo[:, 2])
	r = np.sort(r)
	R = np.mean(r[-1000:])

	return pos, vel, h, m, rho, p, u, matid, R

def bound_load_to_woma(snapshot, remnant_id):
	pos, vel, h, m, rho, p, u, matid, R = load_to_woma(snapshot)
	
	data = sw.load(snapshot)
	bound_id = np.array(data.gas.bound_ids, dtype=np.int32)
	mask = bound_id == remnant_id
	
	return pos[mask], vel[mask], h[mask], m[mask], rho[mask], p[mask], u[mask], matid[mask], R
	
	

