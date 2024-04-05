import requests

url = "http://localhost:8000/animales"

# Crear un animal
print("\n-----Creando un nuevo animal------:")
new_animal = {
    "nombre": "Leon",
    "especie": "Felina",
    "genero": "Masculino",
    "edad": 9,
    "peso": 200
}
post_response = requests.request(method="POST", url=url, json=new_animal)
print(post_response.text)


print("\n----Creando un nuevo animal----:")
new_animal1 = {
    "nombre": "Sapo",
    "especie": "Sapo",
    "genero": "Femenino",
    "edad": 3,
    "peso": 15
}
post_response = requests.request(method="POST", url=url, json=new_animal1)
print(post_response.text)

# Listar todos los animales
print("\n------Listando todos los animales------:")
get_response = requests.request(method="GET", url=url)
print(get_response.text)

# Buscar animales por especie
print("\n------Buscando animales por especie----- (Tigre):")
get_response = requests.request(method="GET", url=f"{url}?especie=Tigre")
print(get_response.text)

# Buscar animales por género
print("\n------Buscando animales por género (Masculino)-----:")
get_response = requests.request(method="GET", url=f"{url}?genero=Masculino")
print(get_response.text)

# Actualizar la información de un animal
print("\n-------Actualizando la información de un animal-------:")
new_animal2 = {
    "nombre": "armadillo",
    "especie": "Dasypusnovemcinctus",
    "genero": "Femenino",
    "edad": 116,
    "peso": 16
}
put_response = requests.request(method="PUT", url=f"{url}/1", json=new_animal2)
print(put_response.text)

# Eliminar un animal
print("\n-----Eliminando un animal-------:")
delete_repsonse = requests.request(method="DELETE", url=f"{url}/2")
print(delete_repsonse.text)