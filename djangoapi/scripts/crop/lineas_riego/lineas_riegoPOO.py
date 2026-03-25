from psycopg.rows import dict_row
from myLib.gestor import tablasPOO


class LineasRiegoPOO(tablasPOO):

    # INSERT
    def insert(self, d: dict):
        wkt = d['geom_wkt']

        if not self.geom_isValid(wkt):
            print("Error: La geometría no es válida")
            self.disconnect()
            return None

        if self.has_interior_intersection('lineas_riego', wkt):
            print("Error: La línea intersecta el interior de una existente.")
            self.disconnect()
            return None

        geom_final    = self.snap_to_grid(wkt)
        material      = d['material']
        diametro_pulg = d['diametro_pulg']
        estado        = d['estado']
        longitud_m    = d['longitud_m']

        cons = """
            INSERT INTO lineas_riego
                (material, diametro_pulg, estado, longitud_m, geom)
            VALUES
                (%s, %s, %s, %s, ST_GeomFromText(%s, %s))
            RETURNING id
        """
        try:
            self.cur.execute(cons, [material, diametro_pulg, estado, longitud_m,
                                    geom_final, self.epsg])
            self.conn.commit()
            new_id = self.cur.fetchone()[0]
            print(f"Línea de riego insertada con id: {new_id}")
            return new_id

        except Exception as e:
            print(f"Error en inserción de línea de riego: {e}")
            self.conn.rollback()
            return None

        finally:
            self.disconnect()

    # SELECT
    def select(self, d: dict, asDict=True):
        id_min = d['id_min']
        cons = """
            SELECT id, material, diametro_pulg, estado, longitud_m,
                   ST_AsText(geom) AS geom_wkt
            FROM lineas_riego
            WHERE id > %s
        """
        try:
            if asDict:
                self.cur = self.conn.cursor(row_factory=dict_row)
            self.cur.execute(cons, [id_min])
            rows = self.cur.fetchall()
            print(f"{len(rows)} línea(s) de riego encontrada(s).")
            return rows

        except Exception as e:
            print(f"Error en select de líneas de riego: {e}")
            return []

        finally:
            self.disconnect()

    # UPDATE
    def update(self, d: dict):
        cons = """
            UPDATE lineas_riego
            SET
                material      = %s,
                diametro_pulg = %s,
                estado        = %s,
                longitud_m    = %s,
                geom          = ST_GeomFromText(%s, %s)
            WHERE id = %s
        """
        try:
            self.cur.execute(cons, [
                d['material'], d['diametro_pulg'], d['estado'], d['longitud_m'],
                d['geom_wkt'], self.epsg, d['id']
            ])
            self.conn.commit()
            print(f"Líneas de riego actualizadas: {self.cur.rowcount} fila(s).")

        except Exception as e:
            print(f"Error en update de líneas de riego: {e}")
            self.conn.rollback()

        finally:
            self.disconnect()

    # DELETE
    def delete(self, d: dict):
        cons = "DELETE FROM lineas_riego WHERE id = %s"
        try:
            self.cur.execute(cons, [d['id']])
            self.conn.commit()
            print(f"Líneas de riego eliminadas: {self.cur.rowcount} fila(s).")

        except Exception as e:
            print(f"Error en delete de líneas de riego: {e}")
            self.conn.rollback()

        finally:
            self.disconnect()


# from psycopg.rows import dict_row
# from myLib.gestor import tablasPOO


# class LineasRiegoPOO(tablasPOO):

#     # INSERT
#     def insert(self, d: dict):
#         cons = """
#             INSERT INTO lineas_riego
#                 (material, diametro_pulg, estado, longitud_m, geom)
#             VALUES
#                 (%s, %s, %s, %s, ST_GeomFromText(%s, %s))
#             RETURNING id
#         """
#         try:
#             self.cur.execute(cons, [
#                 d['material'], d['diametro_pulg'], d['estado'], d['longitud_m'],
#                 d['geom_wkt'], self.epsg
#             ])
#             self.conn.commit()
#             new_id = self.cur.fetchone()[0]
#             print(f"Línea de riego insertada con id: {new_id}")
#             return new_id

#         except Exception as e:
#             print(f"Error en inserción de línea de riego: {e}")
#             self.conn.rollback()
#             return None

#         finally:
#             self.disconnect()

#     # SELECT
#     def select(self, d: dict, asDict=True):
#         cons = """
#             SELECT id, material, diametro_pulg, estado, longitud_m,
#                    ST_AsText(geom) AS geom_wkt
#             FROM lineas_riego
#             WHERE id > %s
#         """
#         try:
#             if asDict:
#                 self.cur = self.conn.cursor(row_factory=dict_row)
#             self.cur.execute(cons, [d['id_min']])
#             rows = self.cur.fetchall()
#             print(f"{len(rows)} línea(s) de riego encontrada(s).")
#             return rows

#         except Exception as e:
#             print(f"Error en select de líneas de riego: {e}")
#             return []

#         finally:
#             self.disconnect()

#     # UPDATE
#     def update(self, d: dict):
#         cons = """
#             UPDATE lineas_riego
#             SET
#                 material      = %s,
#                 diametro_pulg = %s,
#                 estado        = %s,
#                 longitud_m    = %s,
#                 geom          = ST_GeomFromText(%s, %s)
#             WHERE id = %s
#         """
#         try:
#             self.cur.execute(cons, [
#                 d['material'], d['diametro_pulg'], d['estado'], d['longitud_m'],
#                 d['geom_wkt'], self.epsg, d['id']
#             ])
#             self.conn.commit()
#             print(f"Líneas de riego actualizadas: {self.cur.rowcount} fila(s).")

#         except Exception as e:
#             print(f"Error en update de líneas de riego: {e}")
#             self.conn.rollback()

#         finally:
#             self.disconnect()

#     # DELETE
#     def delete(self, d: dict):
#         cons = "DELETE FROM lineas_riego WHERE id = %s"
#         try:
#             self.cur.execute(cons, [d['id']])
#             self.conn.commit()
#             print(f"Líneas de riego eliminadas: {self.cur.rowcount} fila(s).")

#         except Exception as e:
#             print(f"Error en delete de líneas de riego: {e}")
#             self.conn.rollback()

#         finally:
#             self.disconnect()
