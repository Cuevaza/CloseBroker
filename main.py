import time
import config
import csv
from binance.client import Client
from datetime import datetime

# Crear cliente de Binance
api_key = config.api_key
api_secret = config.api_secret
client = Client(api_key, api_secret)

# Crear archivo CSV y escribir encabezados de columna
with open('log balance spot.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Time', 'Balance'])

while True:
    # Obtener la información de la cuenta
    info_cuenta = client.get_account()

    # Variable para almacenar la suma total de los balances en USDT
    suma_total_usdt = 0

    # Calcular la suma total de los balances
    for activo in info_cuenta['balances']:
        # Obtener el balance del activo
        balance = float(activo['free']) + float(activo['locked'])

        if balance > 0:
            # Si el activo es USDT, no necesitamos convertirlo
            if activo['asset'] == 'USDT':
                valor_en_usdt = balance
            else:
                try:
                    # Intentar obtener el último precio del activo en USDT
                    ticker = client.get_symbol_ticker(symbol=f"{activo['asset']}USDT")
                    precio_en_usdt = float(ticker['price'])

                    # Convertir el balance a USDT
                    valor_en_usdt = balance * precio_en_usdt
                except Exception as e:
                    #print(f"No se pudo obtener el precio para {activo['asset']}USDT: {e}")
                    continue

            # Sumar el valor en USDT al total
            suma_total_usdt += valor_en_usdt

    # Imprimir y registrar la suma total de los balances en USDT
    print(f'La suma total de los balances en USDT es {suma_total_usdt}')
    with open('log balance spot.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([time.ctime(), suma_total_usdt])

    # Esperar 10 segundos antes de la próxima iteración
    time.sleep(10)