import configparser
import os
import csv
import logging
from datetime import datetime
from db_connector import upsert_table
from send_email import send_email_with_attachment

# Leer configuración
config = configparser.ConfigParser()
config.read('/config/config.ini')

# loggin registry
log_directory = '/logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file_name = f'/logs/parser_csv_{current_date}.txt'
logging.basicConfig(filename=log_file_name, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Función para verificar si los campos del CSV coinciden con la configuración
def valid_fields(fields_csv, fields_config):
    fields_config = [field.split()[0] for field in fields_config.split(',')]
    print(f"fields_csv {fields_csv}")
    print(f"fields_config {fields_config}")
    return set(fields_csv) == set(fields_config)


def get_table_fields(table_name):
    table_config_section = config['table_config']
    fields_key = table_name + '_fields'

    if fields_key not in table_config_section:
        print(f"La tabla {table_name} no está configurada en config.ini.")
        return None
    
    fields_str = table_config_section[fields_key]
    fields_list = fields_str.split(', ')

    fields = [tuple(field.split(' ', 1)) for field in fields_list]

    print(f"fields {fields}")
    return fields

def parser_csv():
    try:
        # Obtener el listado de carpetas en /data
        folders_csv = os.listdir('/data')
        for folder in folders_csv:
            folder_path = os.path.join('/data', folder)
            csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
            for csv_file in csv_files:
                try:
                    csv_file_path = os.path.join(folder_path, csv_file)
                    print("file_csv ", csv_file_path)
                    with open(csv_file_path, newline='', encoding='utf-8') as file:
                        reader = csv.DictReader(file)
                        headers = reader.fieldnames
                        data = list(reader)
                        #headers = next(reader)
                        table_name = csv_file.split('.')[0]
                        if table_name in config['table_config']:
                            if not valid_fields(headers, config['table_config'][table_name + '_fields']):
                                print(f"Los campos del archivo {csv_file} no coinciden con la configuración.")
                                logging.warning(f"Los campos del archivo {csv_file} no coinciden con la configuración.")
                                return False
                            else:
                                print(f"Los campos del archivo {csv_file} coinciden con la configuración.")
                                fields = get_table_fields(table_name)
                                upsert_table(table_name, data, fields)

                        else:
                            print(f"La tabla {table_name} no está configurada en config.ini.")
                            logging.warning(f"La tabla {table_name} no está configurada en config.ini.")
                except Exception as e:
                    logging.error(f"Error al procesar el archivo {csv_file}: {e}")
        return True
    except Exception as e:
        logging.error(f"Error al obtener el listado de carpetas en /data: {e}")
    finally:
        logging.info("Proceso de parser_csv finalizado.")
        print("Proceso de parser_csv finalizado.")
        send_email_with_attachment(config['email']['to'], "Migración de CSVs", "Proceso finalizado", log_file_name)




