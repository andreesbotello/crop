from psycopg.rows import dict_row

from myLib.connect import connect

EPSG_CODE = 25830


class PlantasPOO():
    def __init__(self):
        self.conn = connect()
        self.cur  = self.conn.cursor()

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    # INSERT
    def insert(self, d: dict):
        variedad          = d['variedad']
        estado_salud      = d['estado_salud']
        fecha_cosecha_est = d['fecha_cosecha_est']
        geom_wkt          = d['geom_wkt']

        cons = """
        INSERT INTO plantas
            (variedad, estado_salud, fecha_cosecha_est, geom)
        VALUES
            (%s, %s, %s,
            st_geometryFromText(%s, %s))
        RETURNING id
        """
        self.cur.execute(cons, [variedad, estado_salud, fecha_cosecha_est,
                                geom_wkt, EPSG_CODE])
        self.conn.commit()
        l = self.cur.fetchall()
        print(f"Planta insertada con id: {l[0][0]}")
        self.disconnect()
        return l[0][0]

    # SELECT
    def select(self, d: dict, asDict=True):
        id_min = d['id_min']

        if asDict:
            self.cur = self.conn.cursor(row_factory=dict_row)

        cons = """
        SELECT
            id, variedad, estado_salud, fecha_cosecha_est,
            st_astext(geom) AS geom_wkt
        FROM
            plantas
        WHERE
            id > %s
        """
        self.cur.execute(cons, [id_min])
        l = self.cur.fetchall()
        print(f"{len(l)} planta(s) encontrada(s).")
        self.disconnect()
        return l

    # UPDATE
    def update(self, d: dict):
        id                = d['id']
        variedad          = d['variedad']
        estado_salud      = d['estado_salud']
        fecha_cosecha_est = d['fecha_cosecha_est']
        geom_wkt          = d['geom_wkt']

        cons = """
        UPDATE plantas
        SET
            variedad          = %s,
            estado_salud      = %s,
            fecha_cosecha_est = %s,
            geom              = st_geometryFromText(%s, %s)
        WHERE
            id = %s
        """
        self.cur.execute(cons, [variedad, estado_salud, fecha_cosecha_est,
                                geom_wkt, EPSG_CODE, id])
        print(f"Filas actualizadas: {self.cur.rowcount}")
        self.conn.commit()
        self.disconnect()

    # DELETE
    def delete(self, d: dict):
        id = d['id']

        cons = """
        DELETE FROM plantas
        WHERE id = %s
        """
        self.cur.execute(cons, [id])
        print(f"Filas eliminadas: {self.cur.rowcount}")
        self.conn.commit()
        self.disconnect()