#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
import requests
import time

# Url desde donde se obtiene los datos a guardar en mongodb
API_URL = 'https://api.coinmarketcap.com/v1/ticker/'

# Función para crear conexión a la bd


def get_db_connection(uri):
    client = pymongo.MongoClient(uri)
    return client.cryptongo


def get_cryptocurrencies_from_api():
    r = requests.get(API_URL)
    if r.status_code == 200:
        result = r.json()
        return result

    raise Exception('API Error')


def first_element(elements):
    return elements[0]  # Devolver el key de elements


def get_hash(value):
    from hashlib import sha512  # Función para encriptar
    return sha512(  # Encripto
        # El string codificado en utf-8, requisito de la librería hash
        value.encode('utf-8')
    ).hexdigest()  # Convertir encriptado en un string para poder ser almacenado posteriormente en bd


# Función para retornar un solo gran string con todos los datos de los items
def get_ticker_hash(ticker_data):
    # Permite ordenar una coleción bajo un criterio
    from collections import OrderedDict
    ticker_data = OrderedDict(
        sorted(  # Función para ordenar cualquier tipo de conjunto de elementos con un criterio
            ticker_data.items(),  # Se le pasa la lista de items a ordenar
            # Sorted manda a llamar a la función first_element, pasándole una tupla (key, value).
            key=first_element
            # Y lo que retorne, será el valor usado para ordenar
        )
    )

    ticker_value = ''  # Donde se guardará el hash final a retornar
    for _, value in ticker_data.items():  # Recorrer la lista de items
        ticker_value += str(value)  # Concatenar el valor del item como string

    return get_hash(ticker_value)  # Encripto string creado


def check_if_exists(db_connection, ticker_data):
    # Creo un hash en base a los datos de la colección del ticker
    ticker_hash = get_ticker_hash(ticker_data)
    if db_connection.tickers.find_one({'ticker_hash': ticker_hash}):
        return True

    return False

# Save ticket


def save_ticker(db_connection, ticker_data=None):
    if not ticker_data:
        return False

    if check_if_exists(db_connection, ticker_data):
        return False

# Convert to integers
    # Creo un hash en base a los datos de la colección del ticker
    ticker_hash = get_ticker_hash(ticker_data)
    # Creo nuevo dato para ser guardado en bd
    ticker_data['ticker_hash'] = ticker_hash
    # Fuerzo conversión de dato a entero
    ticker_data['rank'] = int(ticker_data['rank'])
    # Fuerzo conversión de dato a entero
    ticker_data['last_updated'] = int(ticker_data['last_updated'])

    # Insert a document into the MongoDB collection
    db_connection.tickers.insert_one(ticker_data)
    return True


if __name__ == "__main__":
    while True:
        print("Guardando información en Cryptongo")
        connection = get_db_connection('mongodb://mongodb:27017/')
        tickers = get_cryptocurrencies_from_api()

        for ticker in tickers:
            save_ticker(connection, ticker)
        time.sleep(240)


for ticker in tickers:  # Recorro lista de tickers recibidos
    # Guardo cada ticker en bd, solo si no existe actualmente
    save_ticker(connection, ticker)

print('Tickers almacenados')
