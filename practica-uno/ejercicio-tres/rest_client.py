import requests
url = "http://localhost:8000/"

paciente_1 = {
    "nombre": "Juan",
    "apellido": "Mamani",
    "edad": 48,
    "genero": "Masculino",
    "diagnostico": "Cancer",
    "doctor": "Dra. Paucara"
}
ruta_post_paciente_1 = url + "pacientes"
post_response_paciente_1 = requests.post(ruta_post_paciente_1, json=paciente_1)
print("\n----Nuevo paciente:---:\n")
print(post_response_paciente_1.text)



paciente_2 = {
    "CI": 2,
    "nombre": "Abril",
    "apellido": "Mendez",
    "edad": 28,
    "genero": "Femenino",
    "diagnostico": "Anemia",
    "doctor": "Dr. Mayta"
}
ruta_post_paciente_2 = url + "pacientes"
post_response_paciente_2 = requests.post(ruta_post_paciente_2, json=paciente_2)
print("\n----Nuevo paciente:---:\n")
print(post_response_paciente_2.text)




paciente_3 = {
    "CI": 3,
    "nombre": "Roberto",
    "apellido": "Yujra",
    "edad": 56,
    "genero": "Masculino",
    "diagnostico": "Cancer",
    "doctor": "Dra. Paucara"
}
ruta_post_paciente_3 = url + "pacientes"
post_response_paciente_3 = requests.post(ruta_post_paciente_3, json=paciente_3)
print("\n----Nuevo paciente:---\n")
print(post_response_paciente_3.text)





ruta_get_pacientes = url + "pacientes"
get_response_pacientes = requests.get(ruta_get_pacientes)
print("\n----Lista De pacientes-----:\n")
print(get_response_pacientes.text)




ruta_get_paciente_id_2 = url + "pacientes/1"
get_response_paciente_id_2 = requests.get(ruta_get_paciente_id_2)
print("\n---- Pacientes Con CI-----:\n")
print(get_response_paciente_id_2.text)


ruta_get_pacientes_diabetes = url + "pacientes?diagnostico=Cancer"
get_response_pacientes_diabetes = requests.get(ruta_get_pacientes_diabetes)
print("\n----Pacientes con diagnostico `Cancer`----:\n")
print(get_response_pacientes_diabetes.text)

# Listar a los pacientes que atiende el Doctor `Dra. Paucara`
ruta_get_pacientes_doctor = url + "pacientes?doctor=Dra. Paucara"
get_response_pacientes_doctor = requests.get(ruta_get_pacientes_doctor)
print("\n----Pacientes que son atendidos por `Dra. Paucara`----:\n")
print(get_response_pacientes_doctor.text)



# Actualizar la informacion de un paciente
ruta_put_paciente_1 = url + "pacientes/1"
nuevos_datos_paciente_1 = {
    "nombre": "Julian",
    "edad": 66,
    
}
put_response_paciente_1 = requests.put(ruta_put_paciente_1, json=nuevos_datos_paciente_1)
print("\n----Actualizar informacion del paciente :----\n")
print(put_response_paciente_1.text)



# Eliminar un paciente
ruta_delete_paciente_3 = url + "pacientes/3"
delete_response_paciente_3 = requests.delete(ruta_delete_paciente_3)
print("\n----Eliminar Paciente----:\n")
print(delete_response_paciente_3.text)