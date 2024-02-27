# Material IDs ( = __type_id * __type_factor + __unit_id )
type_factor = 100
type_ANEOS = 4
type_Til = 1
type_HM80 = 2
type_SESAME = 3
type_idg = 0
id_body = 200000000
# Name and ID
MATERIAL_ID_MAP = {
	"ANEOS_iron": type_ANEOS * type_factor + 1,
	"ANEOS_iron_2": type_ANEOS * type_factor + 1 + id_body,
	"ANEOS_alloy": type_ANEOS * type_factor + 2,
	"ANEOS_alloy_2": type_ANEOS * type_factor + 2 + id_body,
	"ANEOS_forsterite": type_ANEOS * type_factor,
	"ANEOS_forsterite_2": type_ANEOS * type_factor + id_body,
	"HM80_HHe": type_HM80 * type_factor,
	"HM80_ice": type_HM80 * type_factor + 1,
	"HM80_rock": type_HM80 * type_factor + 2,
	"HM80_HHe_2": type_HM80 * type_factor + id_body,
	"HM80_ice_2": type_HM80 * type_factor + 1 + id_body,
	"HM80_rock_2": type_HM80 * type_factor + 2 + id_body,
	"SS08_water": type_SESAME * type_factor + 3 + id_body,
	"SS08_water_2": type_SESAME * type_factor + 3 + id_body,
	"AQUA": type_SESAME * type_factor + 4,
	"AQUA_2": type_SESAME * type_factor + 4 + id_body,
	"CMS19_HHe": type_SESAME * type_factor + 7,
	"idg_HHe": type_idg * type_factor,
	"Til_iron": type_Til * type_factor,
	"Til_iron_2": type_Til * type_factor + id_body,
	"Til_granite": type_Til * type_factor + 1,
	"Til_granite_2": type_Til * type_factor + 1 + id_body,
}
# Colour
MATERIAL_COLOUR_MAP = {
	"ANEOS_iron": "tomato", 
	"ANEOS_alloy": "tomato",
	"ANEOS_forsterite": "slategrey",
	"ANEOS_iron_2": "sandybrown",
	"ANEOS_alloy_2": "sandybrown",
	"ANEOS_forsterite_2": "peru",
	"SS08_water": "skyblue",
	"AQUA": "skyblue",
	"AQUA_2": "mediumorchid",
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

