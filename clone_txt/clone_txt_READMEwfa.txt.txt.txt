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
SelectAll: cuenta los elementos de la tabla
SelectAsTuple: muestra los elementos de una tabla como tuplas
SelectAsDict: muestra los elementos en un diccionario clave valor
Delete

eso para las 3 tablas y para las dos metodologias (6x3x2 = 36)
