import requests
import json
import random
import faker

# Crear un objeto faker
fake = faker.Faker()

def generar_juego():
    response_vendedores = requests.get(url_vendedores)
    vendedores = response_vendedores.json()
    vendedor = random.choice(vendedores)

    response_skins = requests.get(url_skins)
    skins = response_skins.json()
    skin = random.choice(skins)

    response_juegos = requests.get(url_juegos)
    juegos = response_juegos.json()
    juego = random.choice(juegos)  

    return {
        "nombre": fake.id(),#random de un nombre predeterminado
        "vendedor_correo": vendedor['usuario_correo'],#random ceo
        "vendedor_nrocuenta" : vendedor['vendedor_nrocuenta'],
        "skin_hash" : skin['hash'],
        "fecha_publicacion" : fake.date(),
        'precio' : fake.random_int(min=10,max=100000),
        'juego_nombre': self.juego['nombre'],
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
    url = "http://localhost:5000/register-post"
    url_vendedores = "http://localhost:5000/show-vendedores"
    url_skins =  "http://localhost:5000/show-skins"
    url_juegos =  "http://localhost:5000/show-juegos"
    
    # Llamada a la funcion para enviar datos
    enviar_datos(url)
