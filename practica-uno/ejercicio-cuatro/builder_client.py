import requests
import json
url = "http://localhost:8000/patients"
headers = {'Content-type': 'application/json'}

print("Creando un nuevo paciente:")
n_paciente = {
    "nombre": "Rodrigo",
    "apellido": "Ticona",
    "edad": 43,
    "genero": "Masculino",
    "diagnostico": "tuberculosis",
    "doctor": "Dr.Yujra" 
}

response = requests.post(url, json=n_paciente, headers=headers)
print(response.json())
print("Creando un nuevo paciente:")
n_paciente = {
    "nombre": "Roberto",
    "apellido": "Pacoricona",
    "edad": 21,
    "genero": "Masculino",
    "diagnostico": " aterosclerosis",
    "doctor": "Dr.Calle" 
}

response = requests.post(url, json=n_paciente, headers=headers)
print(response.json())
print("\n------Listando pacientes:------")
response = requests.get(url, headers=headers)
print(response.json())

print("\n-----Paciente por CI:-----")
response = requests.get(url + "/1", headers=headers)
print(response.json())
print("\n------Pacientes por diagnostico= diabetes:-----")
response = requests.get(url + "?diagnostico=Diabetes", headers=headers)
print(response.json())
print("\n------Actualizando un paciente:------")
nuevo_datos_paciente = {
    "nombre": "Adrian",
    "apellido": "Ticona",
    "edad": 43,
    "genero": "Masculino",
    "diagnostico": "tuberculosis",
    "doctor": "Dr.Yujra"
}
response = requests.put(url + "/1", json=nuevo_datos_paciente, headers=headers)
print(response.json())

print("\n------Eliminando paciente:------")
response = requests.delete(url + "/1")
print(response.json())