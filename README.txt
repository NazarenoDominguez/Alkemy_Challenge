
Uso del programa:
•	Creación de entorno virtual
		Asumiendo que ya tenemos Python instalado y los archivos provistos en GIT, abre una consola en tu editor de código e inserta:
		1.	pip install virtualenv
		2.	python -m venv venv

•	Activación de entorno virtual
		Insertar en consola:
		1.	cd venv/scripts
		2.	activate.bat
		3.	cd ../..

•	instalación de requerimientos
		Insertar en consola:
		1.	pip install -r requirements.txt

•	seteado de base de datos
		en el archivo .env encontraremos:


		DATABASE_HOSTNAME=localhost
		DATABASE_PORT=5432
		DATABASE_PASSWORD=master
		DATABASE_NAME=alkemy_challenge
		DATABASE_USERNAME=postgres


		el password "master" debe ser cambiado al correspondiente de la base de datos de tu maquina
		del mismo modo se puede hacer con el puerto o el nombre de usuario (aunque este ultimo es por defecto)
		
		IMPORTANTE: el programa crea automáticamente la base de datos, si se desea cambiar el nombre no solo basta con cambiarlo en .env
		debes dirigirte al archivo "create_database" de la carpeta sql_files y cambiar el nombre "alkemy_challenge" por aquel que desee 

		Insertar en consola:
		1.	pip install -r requirements.txt

•	ejecución del programa
		Insertar en consola:
		1.	main.py

		se creará la carpeta csv_files donde se encontrarán los archivos correspondiente usando los links de json_files
		se creará la base de datos y todas las tablas de la carpeta sql_files
		se cargarán los datos a las tablas
		se creará un archivo llamada log_file.log en la carpeta loggs
			el mismo contendrá un registro de la actividad de la aplicación

-------------------------------------------------------------------------------------------------------------------------------------------------
estructura del programa

•	paquete data_processing

		modulo alkemy
		contiene la clase principal encargada de crear las carpetas demandadas y procesar los datos, el proceso de datos no está explicito en la clase
		
		modulo decorators
		contiene decoradores que se encargan del procesamiento de cada tabla demandada
			ejemplo: para la tabla que demanda la columna teléfono se encarga de setear el código de área y el teléfono al lado para evitar perdida
			de información ejemplo:: (9999)- 65656565
		para cada una de las 3 tablas requeridas existe un decorador que se encarga de los procesos de limpieza de DataFrame para su posterior carga a DB
		decorador de propósito general "update_postgres_data", este es el encargado de subir los dataframe a base de datos.
		
		modulo logger
		encargado de generar la función logger principal del paquete y reportarlo al archivo log_file


•	paquete models
		__init__
		contiene la conexión a base de datos sql_alkemy como la creación de base de datos

		create
		contiene la función encargada de ejecutar los archivos sql de la carpeta sql_files
		
		tables
		contiene los modelos sql_alkemy de cada tabla, los mismos son muy útiles para hacer consultas a base de datos y se emplean para setear correctamente
		el INSERT de Dataframe.to_sql ya que tal función no está preparada para realizar UPDATE y si se elimina la tabla y se crea con la función los tipos de datos
		y los archivos .sql pierden sentido

		modulo logger
		encargado de generar la función logger principal del paquete y reportarlo al archivo log_file



•	carpeta loggs
		al ejecutarse creará un archivo .log que informará sobre la actividad de la aplicación y emitirá WARNING o CRITICAL si existe algún problema



•	carpeta json_files
		contiene el archivo "links.json"
		este archivo toma los id de los google spreadsheet
		ejemplo::
			los links provistos tienen la siguiente forma:
			https://docs.google.com/spreadsheets/d/1PS2_yAvNVEuSY0gI8Nky73TQMcx_G1i18lm--jOGfAA/edit#gid=514147473
			el id correspondiente al archivo es    1PS2_yAvNVEuSY0gI8Nky73TQMcx_G1i18lm--jOGfAA
			la parte final del link debe ser modificada para permitir la correcta descarga y eso ya esta programado en el paquete data_processing en la clase Alkemy
			se puede poner el id de cualquier otro documento (GOOGLE-spreadsheets) pero se debe programar el modelo, el archivo sql y el decorador para obtener el resultado que deseemos


•	carpeta csv_files
		se creara en la ejecución del programa y la misma contendrá las carpetas y csv seteadas como se dispuso en el challenge

















