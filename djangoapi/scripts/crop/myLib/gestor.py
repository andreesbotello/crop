## utilidades
from myLib.connect import connect
from myLib import p1Settings

class tablasPOO():
    def __init__(self):
        self.conn = connect()
        self.cur  = self.conn.cursor()
        self.epsg = p1Settings.EPSG_CODE

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def geom_isValid(self, geom_wkt):

        query = "SELECT ST_IsValid(ST_GeomFromText(%s, %s));"
        self.cur.execute(query, [geom_wkt, self.epsg])
        return self.cur.fetchone()[0]
    
    def snap_to_grid(self, geom_wkt, size=p1Settings.TOLERANCE):

        query = "SELECT ST_AsText(ST_SnapToGrid(ST_GeomFromText(%s, %s), %s));"
        self.cur.execute(query, [geom_wkt, self.epsg, size])
        return self.cur.fetchone()[0]

    def has_interior_intersection(self, table_name, geom_wkt):

        query = f"""
            SELECT EXISTS (
                SELECT 1 FROM {table_name} 
                WHERE ST_Relate(ST_GeomFromText(%s, %s), geom, 'T********')
            );
        """
        self.cur.execute(query, [geom_wkt, self.epsg])
        return self.cur.fetchone()[0]

    def save_and_close(self, result):

        self.conn.commit()
        self.disconnect()
        return result



