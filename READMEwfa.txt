1. metodología de trabajo
- prompt: yo realizo una solicitud sobre un cambio, nueva metodología o reestructuración o corrección de errores.
- analisis: verificas la información y archivos relacionados
- propuesta: diseñas un implementation_plan
- validación: verifico que hayas comprendido y hago comentarios al respecto y apruebo
- cambios: ejecutas los cambios
- memoria: al final dispones una memoria para mi sobre los cambios realizados
- testing: en algunos casos realizas testing sobre los cambios cuando YO te lo diga

2. preferencias de interacción:
- idioma: español/ingles 
- lenguaje de programación: python, SQL (postgres)
- Nivel de detalle: variable [bajo, medio, alto, resumen tecnico] por defecto medio

3. reglas de edición:
- no editar sin plan aprobado la primera vez que lanzo un prompt, pero si, una vez se este trabajando sobre el mismo plan solo que requiere cambios
- no verificar ni modificar archivos fuera del proyecto
- los cambios desde consola son restringidos unicamente al "humano", tu puedes decir ejecuta esto: "..." o decirme crea esta carpeta o cambia tales permisos
- los comentarios son más de organización nunca de explicación. ej: #1. conectar con la db #2. validar la inserción #2.1. valdiar geometria 

4. contexto del proyecto:
Es una aplicación multiservicio en 3 contenedores docker/linux en un computador windows. actualmente el enfoque es conectar los servicios python (psycopg y django) con los servicios postgres/postgis para gestionar las bases de datos. 
actualmente estamos enfocados en la aplicación 'crops' que contiene las tablas [parcelas, lineas_riego, plantas] estamos generando un sistema robusto para verificar los comandos CRUD de estar 3 tablas para 1. PSYCOPG y para 2. DJANGO, estos dos sistemas de comunación con la base de datos no se mezclan. por lo cual tenemos fundamentalmente 36 funciones
Insert
Update
SelectAsTuple: muestra un solo elemento basado en su ID como tupla
SelectAsDict: muestra un solo elemento basado en su ID como diccionario
SelectAll: cuenta los elementos de la tabla
SelectAsTupleAll: muestra los elementos de una tabla como tuplas
SelectAsDictAll: muestra los elementos en un diccionario clave valor
Delete

eso para las 3 tablas y para las dos metodologias (6x3x2 = 36)

5. ESTRUCTURA
Estructura
Este programa gestiona la conexión de python con un servidos postgres en otro contenedor de docker y se separa fundamentalmente en dos librerias/metodologías.
1.psycopg:
1.1.logica de conexión y configuración:
1.1.1.connect.py
1.1.2.db.py
1.1.3.p1Settings.py
1.2.modelo de las tablas: realizado directamente en postgres con SQL
1.3.tabla maestra que hereda a hijas
1.3.1.gestor.py
1.4.tablas hijas
1.4.1.parcelasPOO.py
1.4.2.lineas_riegoPOO.py
1.4.3.plantasPOO.py
1.5.importador masivo
1.5.1.carga_datos.py
1.6.maestra para concentrar las funciones CRUD
1.6.1.mainPOO.py
2.django:
2.1.logica de conexión y configuración: no tiene externa son internas de django
2.2.modelos de las tablas:
2.2.1.models.py
2.3.tabla maestra:
2.3.1.tablasDJ.py
2.4.tablas hijas:
2.4.1.parcelasDJ.py
2.4.2.lineas_riegoDJ.py
2.4.3.plantasDJ.py
2.5.importador masivo
2.5.1.carga_datosDJ.py
2.6.maestra de concentra funciones CRUD
2.6.1.mainDJ.py
