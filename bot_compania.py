import requests
import json
import random
import faker

# Crear un objeto faker
fake = faker.Faker()

def generar_usuarios():
    return {
        "nombre": fake.nombre(),#random de un nombre predeterminado
        "ceo": fake.name(),#random ceo
    }

def enviar_datos(url):
    # Generar datos falsos y enviar 1000 veces
    for i in range(100):
        # Generar datos falsos
        data = generar_usuarios()

        # Enviar una solicitud POST al servidor
        response = requests.post(url, data=data)

        # Imprimir la respuesta del servidor
        print("Respuesta del servidor:", response.text)

if __name__ == "__main__":
    # URL del servidor Flask
    url = "http://localhost:5000/register-compania"
    
    # Llamada a la funcion para enviar datos
    enviar_datos(url)
