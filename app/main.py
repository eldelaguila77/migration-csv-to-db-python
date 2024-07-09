import configparser
from db_connector import get_db_connections
from parser_csv import parser_csv


def load_config():
    config = configparser.ConfigParser()
    config.read('/config/config.ini')
    return config

config = load_config()

# Ejemplo de cómo acceder a los valores de configuración
db_host = config['database']['host']
task_table_name = config['table_config']['tasks']

def funcion_inicial():
    print("¡Todo está funcionando correctamente!")
    print("db_host", db_host)
    
def check_database_info():
    conn = get_db_connections()
    cursor = conn.cursor()
    query = f"SELECT * FROM {task_table_name}"
    cursor.execute(query)
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("La tabla está vacía.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    funcion_inicial()
    check_database_info()
    parser_csv()