import sys
from parcelas.parcelasPOO    import ParcelasPOO
from lineas_riego.lineas_riegoPOO import LineasRiegoPOO
from plantas.plantasPOO      import PlantasPOO


def main():
    if len(sys.argv) != 3:
        print("Uso: python mainPOO.py <tableName> <functionName>")
        print("  tableName   : parcelas | lineas_riego | plantas")
        print("  functionName: insert | select | selectAsDict | update | delete")
        sys.exit(1)

    tableName, functionName = sys.argv[1], sys.argv[2]

    TABLES    = ["parcelas", "lineas_riego", "plantas"]
    FUNCTIONS = ["insert", "select", "selectAsDict", "update", "delete"]

    if tableName not in TABLES:
        print(f"Error: tabla '{tableName}' no válida. Opciones: {TABLES}")
        sys.exit(1)

    if functionName not in FUNCTIONS:
        print(f"Error: función '{functionName}' no válida. Opciones: {FUNCTIONS}")
        sys.exit(1)

    # ── PARCELAS (Polígono) ────────────────────────────────────────────────────
    if tableName == "parcelas":
        obj = ParcelasPOO()

        if functionName == "insert":
            d = {
                'dueno':         'Juan Garcia',
                'area_m2':       5000.0,
                'cultivo':       'Tomate',
                'fecha_siembra': '2025-05-01',
                'geom_wkt':      'POLYGON ((711624.40527123969513923 4245616.46564004663378, '
                                 '711750.30831353110261261 4245550.72788283508270979, '
                                 '711735.15815491508692503 4245525.56468835100531578, '
                                 '711612.21548844524659216 4245591.73779494967311621, '
                                 '711624.40527123969513923 4245616.46564004663378))',
            }
            obj.insert(d)

        elif functionName == "select":
            obj.select({'id_min': 0}, asDict=False)

        elif functionName == "selectAsDict":
            rows = obj.select({'id_min': 0}, asDict=True)
            for r in rows:
                print(r)

        elif functionName == "update":
            d = {
                'id':            17,
                'dueno':         'prueba update',
                'area_m2':       7500.0,
                'cultivo':       'Tomate UPDATED',
                'fecha_siembra': '2026-03-04',
                'geom_wkt':      'POLYGON ((711616.39484254620037973 4245621.08034353423863649, '
                                 '711603.85678024333901703 4245594.95938040316104889, '
                                 '711484.39690885762684047 4245656.95313290040940046, '
                                 '711489.96938099223189056 4245668.79463618714362383, '
                                 '711521.66281625779811293 4245670.18775422032922506, '
                                 '711616.39484254620037973 4245621.08034353423863649))',
            }
            obj.update(d)

        elif functionName == "delete":
            obj.delete({'id': 16})

    # ── LINEAS_RIEGO (Línea) ───────────────────────────────────────────────────
    elif tableName == "lineas_riego":
        obj = LineasRiegoPOO()

        if functionName == "insert":
            d = {
                'material':      'Acero',
                'diametro_pulg': 8.0,
                'estado':        'Activo',
                'longitud_m':    320.5,
                'geom_wkt':      'LINESTRING (711888.22699886292684823 4244928.61361093167215586, '
                                 '711778.17067420447710901 4244973.19338800851255655, '
                                 '711468.02777196210809052 4245119.99320080131292343, '
                                 '711545.34582282963674515 4245318.07717121299356222, '
                                 '711599.32914663373958319 4245439.10430038627237082, '
                                 '711544.30098430451471359 4245468.88219835516065359, '
                                 '711620.57419664703775197 4245619.774295374751091)',
            }
            obj.insert(d)

        elif functionName == "select":
            obj.select({'id_min': 0}, asDict=False)

        elif functionName == "selectAsDict":
            rows = obj.select({'id_min': 0}, asDict=True)
            for r in rows:
                print(r)

        elif functionName == "update":
            d = {
                'id':            1,
                'material':      'prueba update',
                'diametro_pulg': 3.5,
                'estado':        'Reparacion',
                'longitud_m':    120.0,
                'geom_wkt':      'LINESTRING (711613.58398829190991819 4245605.94549277238547802, '
                                 '711738.37974036775995046 4245539.49586868658661842)',
            }
            obj.update(d)

        elif functionName == "delete":
            obj.delete({'id': 8})

    # ── PLANTAS (Punto) ────────────────────────────────────────────────────────
    elif tableName == "plantas":
        obj = PlantasPOO()

        if functionName == "insert":
            d = {
                'variedad':          'Olivo Arbequina',
                'estado_salud':      'Bueno',
                'fecha_cosecha_est': '2025-11-15',
                'geom_wkt':          'POINT (711734.44366327999159694 4245527.8851424353197217)',
            }
            obj.insert(d)

        elif functionName == "select":
            obj.select({'id_min': 0}, asDict=False)

        elif functionName == "selectAsDict":
            rows = obj.select({'id_min': 0}, asDict=True)
            for r in rows:
                print(r)

        elif functionName == "update":
            d = {
                'id':                1,
                'variedad':          'prueba update',
                'estado_salud':      'Tratamiento',
                'fecha_cosecha_est': '2026-05-20',
                'geom_wkt':          'POINT (711739.76202513591852039 4245537.7621001685038209)',
            }
            obj.update(d)

        elif functionName == "delete":
            obj.delete({'id': 2})


if __name__ == "__main__":
    main()
