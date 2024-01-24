# Material IDs ( = __type_id * __type_factor + __unit_id )
__type_factor = 100
__type_ANEOS = 4
__type_Til = 1
__type_HM80 = 2
__type_SESAME = 3
__type_idg = 0
__id_body = 200000000
# Name and ID
MATERIAL_ID_MAP = {
	"ANEOS_iron": __type_ANEOS * __type_factor + 1,
	"ANEOS_iron_2": __type_ANEOS * __type_factor + 1 + __id_body,
	"ANEOS_alloy": __type_ANEOS * __type_factor + 2,
	"ANEOS_alloy_2": __type_ANEOS * __type_factor + 2 + __id_body,
	"ANEOS_forsterite": __type_ANEOS * __type_factor,
	"ANEOS_forsterite_2": __type_ANEOS * __type_factor + __id_body,
	"HM80_HHe": __type_HM80 * __type_factor,
	"HM80_ice": __type_HM80 * __type_factor + 1,
	"HM80_rock": __type_HM80 * __type_factor + 2,
	"HM80_HHe_2": __type_HM80 * __type_factor + __id_body,
	"HM80_ice_2": __type_HM80 * __type_factor + 1 + __id_body,
	"HM80_rock_2": __type_HM80 * __type_factor + 2 + __id_body,
	"SS08_water": __type_SESAME * __type_factor + 3 + __id_body,
	"SS08_water_2": __type_SESAME * __type_factor + 3 + __id_body,
	"AQUA": __type_SESAME * __type_factor + 4,
	"CMS19_HHe": __type_SESAME * __type_factor + 7,
	"idg_HHe": __type_idg * __type_factor,
	"Til_iron": __type_Til * __type_factor,
	"Til_iron_2": __type_Til * __type_factor + __id_body,
	"Til_granite": __type_Til * __type_factor + 1,
	"Til_granite_2": __type_Til * __type_factor + 1 + __id_body,
}
# Colour
MATERIAL_COLOUR_MAP = {
	"ANEOS_iron": "tomato", 
	"ANEOS_alloy": "tomato",
	"ANEOS_forsterite": "mediumseagreen",
	"ANEOS_iron_2": "sandybrown",
	"ANEOS_alloy_2": "sandybrown",
	"ANEOS_forsterite_2": "pink",
	"SS08_water": "skyblue",
	"AQUA": "skyblue",
	"HM80_HHe": "lightblue",
	"HM80_ice": "aqua",
	"HM80_rock": "slategrey",
	"HM80_HHe_2": "deepskyblue",
	"HM80_ice_2": "darkcyan",
	"HM80_rock_2": "goldenrod",
	"CMS19_HHe": "lavenderblush",
	"idg_HHe": "lavenderblush",
	"Til_iron": "tomato",
	"Til_iron_2": "sandybrown",
	"Til_granite": "mediumseagreen",
	"Til_granite_2": "pink",
}

ID_COLOUR_MAP = {MATERIAL_ID_MAP[mat]: colour for mat, colour in MATERIAL_COLOUR_MAP.items()}

