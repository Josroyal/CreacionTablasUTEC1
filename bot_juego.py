import requests
import json
import random
import faker

# Crear un objeto faker
fake = faker.Faker()

def generar_juego():
    gama = ['alta','baja','epica','media']
    categoria = ['terror','disparos','aventura','deportes','puzzel']
    response = requests.get(url_companias)
    companias = response.json()
    compania = random.choice(companias)

    return {
        "nombre": fake.nombre(),#random de un nombre predeterminado
        "cateogoria": random.choice(categoria),#random ceo
        "gama" : random.choice(gama),
        "compania_nombre" : compania,
    }

def enviar_datos(url):
    # Generar datos falsos y enviar 1000 veces
    for i in range(100):
        # Generar datos falsos
        data = generar_juego()

        # Enviar una solicitud POST al servidor
        response = requests.post(url, data=data)

        # Imprimir la respuesta del servidor
        print("Respuesta del servidor:", response.text)

if __name__ == "__main__":
    # URL del servidor Flask
    url = "http://localhost:5000/register-juego"
    url_vendedores = "http://localhost:5000/show-vendedores"
    url_skins =  "http://localhost:5000/show-skins"
    url_juegos =  "http://localhost:5000/show-juegos"
    
    # Llamada a la funcion para enviar datos
    enviar_datos(url)
