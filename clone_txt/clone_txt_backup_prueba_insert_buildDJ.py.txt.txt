from django.contrib.gis.geos import GEOSGeometry
from django.forms.models import model_to_dict
from django.db import connection
from builds.models import Buildings  # Asegúrate de importar tu modelo correcto

# Configuraciones de entorno (pueden venir de tu p1Settings)
EPSG_CODE = 25830
TOLERANCE = 0.0001

def insert(d: dict):
    """
    Función de inserción que recibe un diccionario, valida la geometría y retorna
    un diccionario estandarizado.
    """
    try:
        # 1. Extraer la geometría en texto del diccionario.
        geom_wkt = d.pop('geom_wkt', None)
        
        if not geom_wkt:
            return {'ok': False, 'message': 'No se proporcionó geom_wkt', 'data': []}

        # 2. Aplicar Snapping 
        with connection.cursor() as cur:
            query = "SELECT ST_AsText(ST_SnapToGrid(ST_GeomFromText(%s, %s), %s));"
            cur.execute(query, [geom_wkt, EPSG_CODE, TOLERANCE])
            snapped_wkt = cur.fetchone()

        # 3. Validar geometría con GEOSGeometry
        g = GEOSGeometry(snapped_wkt, srid=EPSG_CODE)
        if not g.valid:
            return {'ok': False, 'message': 'Geometría inválida', 'data': []}

        # 4. Control topológico: Rechazar polígonos que intersecten con otros
        if Buildings.objects.filter(geom__intersects=g).exists():
            return {'ok': False, 'message': 'Error: La geometría intersecta con otro edificio existente', 'data': []}

        # 5. Inserción de los datos desempaquetando el diccionario
        d['geom'] = g  # Añadimos el objeto validado GEOSGeometry al diccionario para Django
        b = Buildings(**d) # El operador ** mapea las claves del diccionario a los campos del modelo
        b.save()

        # 6. Preparar el retorno convirtiendo el nuevo objeto a diccionario
        b_dict = model_to_dict(b)
        # Convertimos el objeto GEOS de vuelta a texto para que el dict sea serializable
        b_dict['geom'] = g.wkt 

        # 7. Formato de respuesta exacto requerido por el examen
        return {'ok': True, 'message': 'Building inserted', 'data': [b_dict]}

    except Exception as e:
        return {'ok': False, 'message': f'Ocurrió un error: {str(e)}', 'data': []}

def run(*args):
    """
    Función entry-point para probar el script desde runscript.
    """
    # Este es el tipo de diccionario que el profesor te pasará en la demostración
    test_dict = {
        'description': 'Edificio de prueba con diccionario',
        'area': 2500.50,
        'geom_wkt': 'POLYGON ((711624.4 4245616.4, 711750.3 4245550.7, 711735.1 4245525.5, 711612.2 4245591.7, 711624.4 4245616.4))'
    }
    
    # Ejecutamos la función y mostramos el resultado
    resultado = insert(test_dict)
    print(resultado)