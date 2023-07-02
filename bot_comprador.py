import requests
import json
import random
import faker

# Crear un objeto faker
fake = faker.Faker()



def seleecionar_usuario(url_users):
    response = requests.get(url_users)
    users = response.json()
    user = random.choice(users)
    return {
        'usuario_correo' : user['correo'] 
    }
    


def enviar_datos(url):
    # Generar datos falsos y enviar 1000 veces
    for i in range(100):
        # Generar datos falsos
        data = seleecionar_usuario(url_users)

        # Enviar una solicitud POST al servidor
        response = requests.post(url, data=data)

        # Imprimir la respuesta del servidor
        print("Respuesta del servidor:", response.text)

if __name__ == "__main__":
    # URL del servidor Flask
    url = "http://localhost:5000/register-user"
    url_users = "http://localhost:5000/show-user"
    # Llamada a la funcion para enviar datos
    enviar_datos(url)
