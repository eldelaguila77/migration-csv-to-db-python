# db_connector.py
import mysql.connector
import os
import configparser
import logging
from datetime import datetime

# loggin registry
log_directory = '/logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file_name = f'/logs/parser_csv_{current_date}.txt'
logging.basicConfig(filename=log_file_name, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def connect_to_database(db_config):
    conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['name'],
        port=db_config['port']
    )
    return conn

def get_db_connections():
    config = configparser.ConfigParser()
    config.read('/config/config.ini')  # Asegúrate de que la ruta al archivo config.ini sea correcta
    db_config = config['database']  # Accede a la sección 'database' del archivo config.ini
    db1_conn = connect_to_database(db_config)
    return db1_conn

def get_type_mapping():
    # Crear una instancia de ConfigParser
    config = configparser.ConfigParser()
    # Leer el archivo config.ini
    config.read('/config/config.ini')
    # Extraer el mapeo de tipos de la sección TYPE_MAPPING
    type_mapping = {key: eval(value) for key, value in config['TYPE_MAPPING'].items()}
    return type_mapping

def upsert_table(table_name, data, fields):
    type_map = get_type_mapping()
    field_types = {field[0]: type_map[field[1]] for field in fields}
    field_names = [field[0] for field in fields]

    conn = get_db_connections()
    cursor = conn.cursor()

    # Generate the SQL statement for upsert
    sql = f"INSERT INTO {table_name} ({', '.join(field_names)}) VALUES ({', '.join(['%s'] * len(field_names))}) ON DUPLICATE KEY UPDATE "
    sql += ', '.join([f"{field} = VALUES({field})" for field in field_names])

    for row in data:

        converted_values = []
        for field_name in field_names:
            raw_value = row.get(field_name, 'N/A')
            try:
                # Convertir el valor basado en el tipo de campo
                if field_types[field_name] == bool:  # Ajuste para campos booleanos
                    converted_value = 1 if raw_value.lower() in ['true', '1', 'yes'] else 0
                else:
                    converted_value = field_types[field_name](raw_value)
            except Exception as e:
                print(f"Error converting {raw_value} using {field_types.get(field_name, 'Unknown Type')}: {e}")
                logging.error(f"Error converting {raw_value} using {field_types.get(field_name, 'Unknown Type')}: {e}")
                converted_value = None

            converted_values.append(converted_value)
        try:
            cursor.execute(sql, converted_values)
            conn.commit()
        except Exception as e:
            print(f"Error upserting row {row} to {table_name}: {e}")
            logging.error(f"Error upserting row {row} to {table_name}: {e}")
            conn.rollback()
            continue

    # Commit the changes and close the connectiono
    cursor.close()
    conn.close()