# ---------- CHOICES---------------------
import datetime

# Obtener el año actual
current_year = datetime.datetime.now().year

# Generar las opciones para los últimos dos años
CHOICE_EVAL_DESEMPENIO = [
    ("", ""),  # Opción vacía
    ("EXENTO", "EXENTO"),  # Opción EXENTO
]

# Generar opciones para los últimos dos años
for year in range(current_year, current_year - 3, -1):
    CHOICE_EVAL_DESEMPENIO.extend(
        [
            (f"{year} - DESEMPEÑO DESTACADO", f"{year} - DESEMPEÑO DESTACADO"),
            (f"{year} - DESEMPEÑO BUENO", f"{year} - DESEMPEÑO BUENO"),
            (f"{year} - DESEMPEÑO BAJO", f"{year} - DESEMPEÑO BAJO"),
        ]
    )

CHOICE_NIVEL_EDUCATIVO = [
    ("", ""),
    ("Secundario incompleto", "Secundario incompleto"),
    ("Secundario completo", "Secundario completo"),
    ("Terciario incompleto", "Terciario incompleto"),
    ("Terciario completo", "Terciario completo"),
    ("Universitario incompleto", "Universitario incompleto"),
    ("Universitario completo", "Universitario completo"),
    ("Posgrado", "Posgrado"),
]


CHOICE_SINO = [("", ""), ("SI", "SI"), ("NO", "NO")]

CHOICE_ESTADO_CIVIL = [
    ("", ""),
    ("Soltero/a", "Soltero/a"),
    ("Casado/a", "Casado/a"),
    ("Divorciado/a", "Divorciado/a"),
    ("Viudo/a", "Viudo/a"),
    ("Separado/a", "Separado/a"),
    ("Otro", "Otro"),
]


CHOICE_SEXO = [
    ("", ""),
    ("Masculino", "Masculino"),
    ("Femenino", "Femenino"),
    ("Otro", "Otro"),
]

CHOICE_GO_EQUIPO = [
    ("", ""),
    ("GO Coord de Serv.", "GO Coord de Serv."),
    ("U.A.C. N° 01", "U.A.C. N° 01"),
    ("U.A.C. N° 02", "U.A.C. N° 02"),
    ("U.A.C. N° 03", "U.A.C. N° 03"),
    ("U.A.C. N° 04", "U.A.C. N° 04"),
    ("U.A.C. N° 05", "U.A.C. N° 05"),
    ("U.A.C. N° 06", "U.A.C. N° 06"),
    ("U.A.C. N° 07", "U.A.C. N° 07"),
    ("U.A.C. N° 08", "U.A.C. N° 08"),
    ("U.A.C. N° 09", "U.A.C. N° 09"),
    ("U.A.C. N° 10", "U.A.C. N° 10"),
    ("U.A.C. N° 11", "U.A.C. N° 11"),
    ("U.A.C. N° 12", "U.A.C. N° 12"),
    ("U.A.C. N° 13", "U.A.C. N° 13"),
    ("U.A.C. N° 14", "U.A.C. N° 14"),
    ("U.A.C. N° 15", "U.A.C. N° 15"),
]

CHOICE_PROVINCIAS = [
    (None, "Provincia"),
    ("CABA", "CABA"),
    ("Buenos Aires", "Buenos Aires"),
    ("Catamarca", "Catamarca"),
    ("Chaco", "Chaco"),
    ("Chubut", "Chubut"),
    ("Córdoba", "Córdoba"),
    ("Corrientes", "Corrientes"),
    ("Entre Ríos", "Entre Ríos"),
    ("Formosa", "Formosa"),
    ("Jujuy", "Jujuy"),
    ("La Pampa", "La Pampa"),
    ("La Rioja", "La Rioja"),
    ("Mendoza", "Mendoza"),
    ("Misiones", "Misiones"),
    ("Neuquén", "Neuquén"),
    ("Río Negro", "Río Negro"),
    ("Salta", "Salta"),
    ("San Juan", "San Juan"),
    ("San Luis", "San Luis"),
    ("Santa Cruz", "Santa Cruz"),
    ("Santa Fe", "Santa Fe"),
    ("Santiago del Estero", "Santiago del Estero"),
    ("Tierra del Fuego", "Tierra del Fuego"),
    ("Tucumán", "Tucumán"),
]

CHOICE_COMUNA = [
    ("", ""),
    ("1", "COMUNA 1"),
    ("2", "COMUNA 2"),
    ("3", "COMUNA 3"),
    ("4", "COMUNA 4"),
    ("5", "COMUNA 5"),
    ("6", "COMUNA 6"),
    ("7", "COMUNA 7"),
    ("8", "COMUNA 8"),
    ("9", "COMUNA 9"),
    ("10", "COMUNA 10"),
    ("11", "COMUNA 11"),
    ("12", "COMUNA 12"),
    ("13", "COMUNA 13"),
    ("14", "COMUNA 14"),
    ("15", "COMUNA 15"),
]


CHOICE_TIPO_CONTRATACION = [
    ("", ""),
    ("LOYS", "LOYS"),
    ("PLANTA", "PLANTA"),
    ("PLANTA COMUNA", "PLANTA COMUNA"),
    ("PLANTA TRANSITORIA", "PLANTA TRANSITORIA"),
    ("CONTRATO COMUNA", "CONTRATO COMUNA"),
    ("URS", "URS"),
]


CHOICE_SEDES = [
    ("", ""),
    ("COMUNA 1", "COMUNA 1"),
    ("COMUNA 2", "COMUNA 2"),
    ("COMUNA 3", "COMUNA 3"),
    ("COMUNA 4", "COMUNA 4"),
    ("COMUNA 5", "COMUNA 5"),
    ("COMUNA 6", "COMUNA 6"),
    ("COMUNA 7", "COMUNA 7"),
    ("COMUNA 8", "COMUNA 8"),
    ("COMUNA 9", "COMUNA 9"),
    ("COMUNA 10", "COMUNA 10"),
    ("COMUNA 11", "COMUNA 11"),
    ("COMUNA 12", "COMUNA 12"),
    ("COMUNA 13", "COMUNA 13"),
    ("COMUNA 14", "COMUNA 14"),
    ("COMUNA 15", "COMUNA 15"),
]


CHOICE_EVENTO_MODALIDAD = [
    (None, ""),
    ("PRESENCIAL", "PRESENCIAL"),
    ("VIRTUAL", "VIRTUAL"),
]

CHOICE_TRASPASOS = [
    ("", ""),
    ("PERMANENTE", "PERMANENTE"),
    ("TEMPORARIO", "TEMPORARIO"),
]


CHOICE_TIPO_LICENCIA = [
    ("", ""),
    ("ORDINARIA", "ORDINARIA"),
    ("ESPECIAL", "ESPECIAL"),
]

CHOICE_MOTIVO_LICENCIA = [
    ("", ""),
    ("SALUD", "SALUD"),
    ("SALUD FAMILIAR", "SALUD FAMILIAR"),
    ("MATERNIDAD/PATERNIDAD", "MATERNIDAD/PATERNIDAD"),
    ("MOTIVOS PERSONALES", "MOTIVOS PERSONALES"),
    ("DIAS DE ESTUDIO", "DIAS DE ESTUDIO"),
    ("OTROS", "OTROS"),
]
