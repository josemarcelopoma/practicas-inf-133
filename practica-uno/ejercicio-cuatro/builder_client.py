import requests
import json

url = "http://localhost:8000/patients"
headers = {'Content-type': 'application/json'}

# Crear un paciente
print("Creando un nuevo paciente:")
nuevo_paciente = {
    "nombre": "Juan",
    "apellido": "Perez",
    "edad": 30,
    "genero": "Masculino",
    "diagnostico": "Resfriado",
    "doctor": "Dr.Garcia"  # Añadir el atributo "doctor"
}
response = requests.post(url, json=nuevo_paciente, headers=headers)
print(response.json())

# Listar todos los pacientes
print("\nListando todos los pacientes:")
response = requests.get(url, headers=headers)
print(response.json())

# Buscar pacientes por CI
print("\nBuscando paciente por CI:")
response = requests.get(url + "/1", headers=headers)
print(response.json())

# Listar a los pacientes que tienen diagnostico de `Diabetes`
print("\nListando pacientes con diagnóstico de Diabetes:")
response = requests.get(url + "?diagnostico=Diabetes", headers=headers)
print(response.json())

# Listar a los pacientes que atiende el Doctor `Pedro Pérez`
print("\nListando pacientes atendidos por el Doctor Pedro Pérez:")
response = requests.get(url + "?doctor=Pedro Pérez", headers=headers)
print(response.json())

# Actualizar la información de un paciente
print("\nActualizando la información de un paciente:")
nuevo_datos_paciente = {
    "nombre": "Juanita",
    "apellido": "Perez",
    "edad": 30,
    "genero": "Femenino",
    "diagnostico": "Resfriado",
    "doctor": "Dr.Garcia"
}
response = requests.put(url + "/1", json=nuevo_datos_paciente, headers=headers)
print(response.json())

# Eliminar un paciente
print("\nEliminando un paciente:")
response = requests.delete(url + "/1")
print(response.json())