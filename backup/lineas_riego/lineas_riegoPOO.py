from psycopg.rows import dict_row
from myLib.connect import connect

EPSG_CODE = 25830


class LineasRiegoPOO():
    def __init__(self):
        self.conn = connect()
        self.cur  = self.conn.cursor()

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    # INSERT
    def insert(self, d: dict):
        material      = d['material']
        diametro_pulg = d['diametro_pulg']
        estado        = d['estado']
        longitud_m    = d['longitud_m']
        geom_wkt      = d['geom_wkt']

        cons = """
        INSERT INTO lineas_riego
            (material, diametro_pulg, estado, longitud_m, geom)
        VALUES
            (%s, %s, %s, %s,
            st_geometryFromText(%s, %s))
        RETURNING id
        """
        self.cur.execute(cons, [material, diametro_pulg, estado, longitud_m,
                                geom_wkt, EPSG_CODE])
        self.conn.commit()
        l = self.cur.fetchall()
        print(f"Línea de riego insertada con id: {l[0][0]}")
        self.disconnect()
        return l[0][0]

    # SELECT
    def select(self, d: dict, asDict=True):
        id_min = d['id_min']

        if asDict:
            self.cur = self.conn.cursor(row_factory=dict_row)

        cons = """
        SELECT
            id, material, diametro_pulg, estado, longitud_m,
            st_astext(geom) AS geom_wkt
        FROM
            lineas_riego
        WHERE
            id > %s
        """
        self.cur.execute(cons, [id_min])
        l = self.cur.fetchall()
        print(f"{len(l)} línea(s) de riego encontrada(s).")
        self.disconnect()
        return l

    # UPDATE
    def update(self, d: dict):
        id            = d['id']
        material      = d['material']
        diametro_pulg = d['diametro_pulg']
        estado        = d['estado']
        longitud_m    = d['longitud_m']
        geom_wkt      = d['geom_wkt']

        cons = """
        UPDATE lineas_riego
        SET
            material      = %s,
            diametro_pulg = %s,
            estado        = %s,
            longitud_m    = %s,
            geom          = st_geometryFromText(%s, %s)
        WHERE
            id = %s
        """
        self.cur.execute(cons, [material, diametro_pulg, estado, longitud_m,
                                geom_wkt, EPSG_CODE, id])
        print(f"Filas actualizadas: {self.cur.rowcount}")
        self.conn.commit()
        self.disconnect()

    # DELETE
    def delete(self, d: dict):
        id = d['id']

        cons = """
        DELETE FROM lineas_riego
        WHERE id = %s
        """
        self.cur.execute(cons, [id])
        print(f"Filas eliminadas: {self.cur.rowcount}")
        self.conn.commit()
        self.disconnect()