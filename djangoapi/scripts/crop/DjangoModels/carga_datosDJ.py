from scripts.crop.DjangoModels.parcelas.parcelasDJ import ParcelasDJ
from scripts.crop.DjangoModels.lineas_riego.lineas_riegoDJ import LineasRiegoDJ
from scripts.crop.DjangoModels.plantas.plantasDJ import PlantasDJ
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.utils.dateparse import parse_datetime

data_parcelas = [
    {'dueno': 'Juan Garcia', 'cultivo': 'Tomate', 'fecha_siembra': '2025-05-01 00:00:00', 'geom': 'POLYGON((711624.40527123969513923 4245616.46564004663378, 711750.30831353110261261 4245550.72788283508270979, 711735.15815491508692503 4245525.56468835100531578, 711612.21548844524659216 4245591.73779494967311621, 711624.40527123969513923 4245616.46564004663378))'},
    {'dueno': 'Ana Belen', 'cultivo': 'Tomate', 'fecha_siembra': '2025-04-15 00:00:00', 'geom': 'POLYGON((711616.39484254620037973 4245621.08034353423863649, 711603.85678024333901703 4245594.95938040316104889, 711484.39690885762684047 4245656.95313290040940046, 711489.96938099223189056 4245668.79463618714362383, 711521.66281625779811293 4245670.18775422032922506, 711616.39484254620037973 4245621.08034353423863649))'},
    {'dueno': 'Luis Perez', 'cultivo': 'Lechuga', 'fecha_siembra': '2025-06-10 00:00:00', 'geom': 'POLYGON((711723.49079138319939375 4245525.82589798327535391, 711710.95272908033803105 4245499.70493485312908888, 711595.32393228716682643 4245559.26073079090565443, 711609.25511262367945164 4245586.42653244733810425, 711723.49079138319939375 4245525.82589798327535391))'},
    {'dueno': 'Marta Ruiz', 'cultivo': 'Brocoli', 'fecha_siembra': '2025-03-20 00:00:00', 'geom': 'POLYGON((711453.57417236303444952 4245665.57305073365569115, 711601.59296343859750777 4245589.99639740772545338, 711587.31350359367206693 4245563.87543427664786577, 711448.69825924525503069 4245634.57617448456585407, 711453.57417236303444952 4245665.57305073365569115))'},
    {'dueno': 'Carlos Saenz', 'cultivo': 'Lechuga', 'fecha_siembra': '2025-02-10 00:00:00', 'geom': 'POLYGON((711592.71183597412891686 4245555.08137669041752815, 711702.07160161586944014 4245500.0532143609598279, 711687.44386226253118366 4245475.67364877182990313, 711580.87033268809318542 4245528.96041355933994055, 711592.71183597412891686 4245555.08137669041752815))'},
    {'dueno': 'Elena Cano', 'cultivo': 'Pimiento', 'fecha_siembra': '2025-01-05 00:00:00', 'geom': 'POLYGON((711585.22382654319517314 4245558.9995211586356163, 711572.68576424033381045 4245533.57511704508215189, 711445.56374366953969002 4245598.00682610087096691, 711451.1362158041447401 4245629.00370234996080399, 711585.22382654319517314 4245558.9995211586356163))'}
]

data_lineas = [
    {'material': 'Acero', 'diametro_pulg': 8.0, 'estado': 'Activo', 'geom': 'LINESTRING(711888.22699886292684823 4244928.61361093167215586, 711778.17067420447710901 4244973.19338800851255655, 711468.02777196210809052 4245119.99320080131292343, 711545.34582282963674515 4245318.07717121299356222, 711599.32914663373958319 4245439.10430038627237082, 711544.30098430451471359 4245468.88219835516065359, 711620.57419664703775197 4245619.774295374751091)'},
    {'material': 'PEAD', 'diametro_pulg': 3.0, 'estado': 'Activo', 'geom': 'LINESTRING(711613.58398829190991819 4245605.94549277238547802, 711738.37974036775995046 4245539.49586868658661842)'},
    {'material': 'PVC', 'diametro_pulg': 1.0, 'estado': 'Mantenimiento', 'geom': 'LINESTRING(711738.37974036775995046 4245539.49586868658661842, 711744.30049201066140085 4245551.66388401202857494)'},
    {'material': 'PVC', 'diametro_pulg': 1.0, 'estado': 'Inactivo', 'geom': 'LINESTRING(711738.37974036775995046 4245539.49586868658661842, 711732.54605860181618482 4245528.32915694825351238)'},
    {'material': 'PVC', 'diametro_pulg': 1.0, 'estado': 'Activo', 'geom': 'LINESTRING(711735.77133060281630605 4245540.88476090040057898, 711741.77546557469759136 4245552.70872253738343716)'},
    {'material': 'PVC', 'diametro_pulg': 1.0, 'estado': 'Activo', 'geom': 'LINESTRING(711735.77133060281630605 4245540.88476090040057898, 711730.54345142841339111 4245529.98348461370915174)'}
]

data_plantas = [
    {'variedad': 'Olivo Arbequina', 'estado_salud': 'Bueno', 'fecha_cosecha_est': '2025-11-15 00:00:00', 'geom': 'POINT(711734.44366327999159694 4245527.8851424353197217)'},
    {'variedad': 'Naranjo Valencia', 'estado_salud': 'Regular', 'fecha_cosecha_est': '2025-12-01 00:00:00', 'geom': 'POINT(711735.27940585731994361 4245529.55662759020924568)'},
    {'variedad': 'Limonero Verna', 'estado_salud': 'Excelente', 'fecha_cosecha_est': '2025-10-20 00:00:00', 'geom': 'POINT(711736.11514843464829028 4245531.15213614702224731)'},
    {'variedad': 'Almendro Marcona', 'estado_salud': 'Enfermo', 'fecha_cosecha_est': '2025-09-05 00:00:00', 'geom': 'POINT(711736.95089101197663695 4245532.6716681057587266)'},
    {'variedad': 'Aguacate Hass', 'estado_salud': 'Bueno', 'fecha_cosecha_est': '2025-08-12 00:00:00', 'geom': 'POINT(711737.71065699146129191 4245534.1152234673500061)'},
    {'variedad': 'Vid Moscatel', 'estado_salud': 'Bueno', 'fecha_cosecha_est': '2025-09-30 00:00:00', 'geom': 'POINT(711738.69835276470985264 4245535.93866181746125221)'}
]

def _aware_datetime(value):
    if not isinstance(value, str):
        return value
    dt = parse_datetime(value)
    if dt is None:
        return value
    if timezone.is_naive(dt):
        return timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


def _prepare_item(item):
    data = item.copy()
    for field_name in ('fecha_siembra', 'fecha_cosecha_est'):
        if field_name in data:
            data[field_name] = _aware_datetime(data[field_name])
    return data


def run(*args):
    """Función de entrada para runscript."""
    p_api = ParcelasDJ()
    l_api = LineasRiegoDJ()
    pl_api = PlantasDJ()

    print("--- Iniciando carga masiva en Django (PostGIS) ---")

    # 1. Carga de Parcelas
    print("\nProcesando parcelas...")
    for item in data_parcelas:
        data = _prepare_item(item)
        res = p_api.insert(data)
        print(f"Parcela de {data['dueno']}: {res}")

    # 2. Carga de Líneas
    print("\nProcesando líneas de riego...")
    for item in data_lineas:
        data = _prepare_item(item)
        res = l_api.insert(data)
        print(f"Línea {data['material']}: {res}")

    # 3. Carga de Plantas
    print("\nProcesando plantas...")
    for item in data_plantas:
        data = _prepare_item(item)
        res = pl_api.insert(data)
        print(f"Planta {data['variedad']}: {res}")

    print("\n--- Carga masiva Django finalizada con éxito ---")


if __name__ == "__main__":
    run()