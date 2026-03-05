import sys
from parcelas.parcelasPOO import ParcelasPOO
from lineas_riego.lineas_riegoPOO import LineasRiegoPOO
from plantas.plantasPOO import PlantasPOO


def main():
    # sys.argv[0] es siempre el nombre del archivo (main.py)
    # Por eso verificamos que haya al menos 3 elementos (nombre + p1 + p2)
    if len(sys.argv) == 3:
        tableName    = sys.argv[1]
        functionName = sys.argv[2]
    else:
        print("Error: Debes indicar dos parámetros: tableName y functionName.")
        sys.exit(0)

    if tableName not in ["parcelas", "lineas_riego", "plantas"]:
        print("Error: Los nombres de tabla disponibles son parcelas, lineas_riego, plantas")
        sys.exit(0)

    if functionName not in ["insert", "select", "selectAsDict", "update", "delete"]:
        print("Error: Las funciones disponibles son insert, select, selectAsDict, update, delete")
        sys.exit(0)

    # PARCELAS  (Poligono)
    if tableName == "parcelas":
        b = ParcelasPOO()
        if functionName == "insert":
            d = {'dueno': 'Juan Garcia', 'area_m2': 5000.0, 'cultivo': 'Tomate', 'fecha_siembra': '2025-05-01', 'geom_wkt': 'POLYGON ((711624.40527123969513923 4245616.46564004663378, 711750.30831353110261261 4245550.72788283508270979, 711735.15815491508692503 4245525.56468835100531578, 711612.21548844524659216 4245591.73779494967311621, 711624.40527123969513923 4245616.46564004663378))'}

            b.insert(d)
            print(f"Inserción de parcela de {d['dueno']} completada.")

        elif functionName == "select":
            d = {'id_min': 0}
            b.select(d, asDict=False)
        elif functionName == "selectAsDict":
            d = {'id_min': 0}
            b.select(d, asDict=True)
        elif functionName == "update":
            d = {
            'id':            14,  # ID autoincremental generado previamente
            'dueno':         'prueba update',
            'area_m2':       7500.0,
            'cultivo':       'Tomate UPDATED',
            'fecha_siembra': '2026-03-04',
            'geom_wkt':      'POLYGON ((711616.39484254620037973 4245621.08034353423863649, 711603.85678024333901703 4245594.95938040316104889, 711484.39690885762684047 4245656.95313290040940046, 711489.96938099223189056 4245668.79463618714362383, 711521.66281625779811293 4245670.18775422032922506, 711616.39484254620037973 4245621.08034353423863649))'
            }
            b.update(d)
            print("Update: Dueño cambiado a 'prueba update' en parcelas.")

        elif functionName == "delete":
            d = {'id': 15}
            b.delete(d)

    # LINEAS_RIEGO  (Line)
    elif tableName == "lineas_riego":
        l = LineasRiegoPOO()
        if functionName == "insert":
            d = {'material': 'Acero', 'diametro_pulg': 8.0, 'estado': 'Activo', 'longitud_m': 320.5, 'geom_wkt': 'LINESTRING (711888.22699886292684823 4244928.61361093167215586, 711778.17067420447710901 4244973.19338800851255655, 711468.02777196210809052 4245119.99320080131292343, 711545.34582282963674515 4245318.07717121299356222, 711599.32914663373958319 4245439.10430038627237082, 711544.30098430451471359 4245468.88219835516065359, 711620.57419664703775197 4245619.774295374751091)'}

            l.insert(d)
            print(f"Inserción de líneas de riego completada.")

        elif functionName == "select":
            d = {'id_min': 0}
            l.select(d, asDict=False)
        elif functionName == "selectAsDict":
            d = {'id_min': 0}
            l.select(d, asDict=True)
        elif functionName == "update":
            d = {
            'id':            1,
            'material':      'prueba update',
            'diametro_pulg': 3.5,
            'estado':        'Reparacion',
            'longitud_m':    120.0,
            'geom_wkt':      'LINESTRING (711613.58398829190991819 4245605.94549277238547802, 711738.37974036775995046 4245539.49586868658661842)'
            }
            l.update(d)
            print("Update: Material cambiado a 'prueba update' en lineas_riego.")

        elif functionName == "delete":
            d = {'id': 2}
            l.delete(d)

    # PLANTAS  (Point)
    elif tableName == "plantas":
        p = PlantasPOO()
        if functionName == "insert":
            d = {'variedad': 'Olivo Arbequina', 'estado_salud': 'Bueno', 'fecha_cosecha_est': '2025-11-15', 'geom_wkt': 'POINT (711734.44366327999159694 4245527.8851424353197217)'}

            p.insert(d)
            print(f"Inserción de {d['variedad']}")

        elif functionName == "select":
            d = {'id_min': 0}
            p.select(d, asDict=False)
        elif functionName == "selectAsDict":
            d = {'id_min': 0}
            p.select(d, asDict=True)
        elif functionName == "update":
            d = {
            'id':                1,
            'variedad':          'prueba update',
            'estado_salud':      'Tratamiento',
            'fecha_cosecha_est': '2026-05-20',
            'geom_wkt':          'POINT (711739.76202513591852039 4245537.7621001685038209)'
            }
            p.update(d)
            print("Update: Variedad cambiada a 'prueba update' en plantas.")

        elif functionName == "delete":
            d = {'id': 2}
            p.delete(d)


if __name__ == "__main__":
    main()