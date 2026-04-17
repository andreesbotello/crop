import sys
from scripts.crop.DjangoModels.parcelas.parcelasDJ import ParcelasDJ
from scripts.crop.DjangoModels.lineas_riego.lineas_riegoDJ import LineasRiegoDJ
from scripts.crop.DjangoModels.plantas.plantasDJ import PlantasDJ

def run(*args):
    """
    Uso: python manage.py runscript scripts.crop.mainDJ --script-args <tableName> <functionName>
    Ejemplo: python manage.py runscript scripts.crop.mainDJ --script-args parcelas insert
    """
    if len(args) != 2:
        print("Error: Se requieren 2 argumentos: <tableName> <functionName>")
        print("Tablas: parcelas | lineas_riego | plantas")
        print("Funciones: insert | selectAll | selectAsDict | selectAsDictAll | selectAsTuple | selectAsTupleAll | update | delete")
        return

    tableName, functionName = args[0], args[1]

    # ── CONFIGURACIÓN DE INSTANCIAS ──
    apis = {
        "parcelas": ParcelasDJ(),
        "lineas_riego": LineasRiegoDJ(),
        "plantas": PlantasDJ()
    }

    if tableName not in apis:
        print(f"Error: Tabla '{tableName}' no válida.")
        return

    obj = apis[tableName]

    # ── LÓGICA DE EJECUCIÓN (Adaptada a models.py) ──

    # 1. PARCELAS
    if tableName == "parcelas":
        if functionName == "insert":
            d = {
                'dueno': 'Juan Garcia',
                'cultivo': 'Tomate',
                'fecha_siembra': '2025-05-01 00:00:00',
                'geom': 'POLYGON ((711624.40527123969513923 4245616.46564004663378, '
                                 '711750.30831353110261261 4245550.72788283508270979, '
                                 '711735.15815491508692503 4245525.56468835100531578, '
                                 '711612.21548844524659216 4245591.73779494967311621, '
                                 '711624.40527123969513923 4245616.46564004663378))'
            }
            print(obj.insert(d))

        elif functionName == "update":
            d = {
                'id': 7,
                'dueno': 'Actualizado Django',
                'cultivo': 'Tomate UPDATED',
                'geom': 'POLYGON ((711624.40527123969513923 4245616.46564004663378, '
                                 '711750.30831353110261261 4245550.72788283508270979, '
                                 '711735.15815491508692503 4245525.56468835100531578, '
                                 '711612.21548844524659216 4245591.73779494967311621, '
                                 '711624.40527123969513923 4245616.46564004663378))'
            }
            print(obj.update(d))

    # 2. LINEAS DE RIEGO
    elif tableName == "lineas_riego":
        if functionName == "insert":
            d = {
                'material': 'Acero',
                'diametro_pulg': 8.0,
                'estado': 'Activo',
                'geom': 'LINESTRING (711888.22699886292684823 4244928.61361093167215586, '
                                 '711778.17067420447710901 4244973.19338800851255655, '
                                 '711468.02777196210809052 4245119.99320080131292343, '
                                 '711545.34582282963674515 4245318.07717121299356222, '
                                 '711599.32914663373958319 4245439.10430038627237082, '
                                 '711544.30098430451471359 4245468.88219835516065359, '
                                 '711620.57419664703775197 4245619.774295374751091)'
            }
            print(obj.insert(d))

        elif functionName == "update":
            d = {
                'id': 6,
                'material': 'prueba update',
                'diametro_pulg': 4.5,
                'estado': 'Reparacion',
                'geom': 'LINESTRING (711888.22699886292684823 4244928.61361093167215586, '
                                 '711778.17067420447710901 4244973.19338800851255655, '
                                 '711468.02777196210809052 4245119.99320080131292343, '
                                 '711545.34582282963674515 4245318.07717121299356222, '
                                 '711599.32914663373958319 4245439.10430038627237082, '
                                 '711544.30098430451471359 4245468.88219835516065359, '
                                 '711620.57419664703775197 4245619.774295374751091)'
            }
            print(obj.update(d))

    # 3. PLANTAS
    elif tableName == "plantas":
        if functionName == "insert":
            d = {
                'variedad': 'Olivo Arbequina',
                'estado_salud': 'Bueno',
                'fecha_cosecha_est': '2025-11-15 00:00:00',
                'geom': 'POINT (711734.44366327999159694 4245527.8851424353197217)'
            }
            print(obj.insert(d))

        elif functionName == "update":
            d = {
                'id': 7,
                'variedad': 'prueba update',
                'estado_salud': 'Tratamiento',
                'fecha_cosecha_est': '2026-01-20 00:00:00',
                'geom': 'POINT (711734.44366327999159694 4245527.8851424353197217)'
            }
            print(obj.update(d))

    # ── FUNCIONES GENÉRICAS (Heredadas de TablasDJ) ──
    if functionName == "selectAll":
        total = obj.selectAll(id_min=0)
        print(total)

    elif functionName == "selectAsDictAll":
        rows = obj.selectAsDictAll(id_min=0)
        for r in rows: print(r)

    elif functionName == "selectAsDict":
        row = obj.selectAsDict(_id=1)
        print(row)

    elif functionName == "selectAsTupleAll":
        rows = obj.selectAsTupleAll(id_min=0)
        for r in rows: print(r)

    elif functionName == "selectAsTuple":
        row = obj.selectAsTuple(_id=1)
        print(row)

    elif functionName == "delete":
        print(obj.delete({'id': 6}))
