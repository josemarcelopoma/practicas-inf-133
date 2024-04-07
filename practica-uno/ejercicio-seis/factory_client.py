import requests
import json
url = "http://localhost:8000/animales"
headers = {"Content-Type": "application/json"}
print("\n-----nuevos animales:-----")
nuevo_a_dat = {
    "animal_type": "reptil",
    "nombre": "lagartija",
    "especies": "Teiidae",
    "Genero": "masculino",
    "Edada": 4,
    "Altura": 3
}
print("\n-----creando animal:-----")
response = requests.post(url=url, json=nuevo_a_dat, headers=headers)
print("post:", response.json())

nuevo_a_dat = {
    "animal_type": "pez",
    "nombre": "mantarraya",
    "especies": "Manta birostris",
    "Genero": "masculino",
    "Edada": 18,
    "Altura": 3
}
print("\n-----creando animal:-----")
response = requests.post(url=url, json=nuevo_a_dat, headers=headers)
print("post:", response.json())

actualizar_animal_a = {
    "nombre": "sapo",
    "altura": 2
}
print("\n-----actualizar animal :-----")
update_response = requests.put(f"{url}/0", json=actualizar_animal_a, headers=headers)
print("put:", update_response.json())

print("\n-----Obtener animal :-----")
get_response = requests.get(url)
print("get:", get_response.json())

print("\n-----eliminar animal:-----")
delete_response = requests.delete(f"{url}/0")
print("Delet:", delete_response.json())