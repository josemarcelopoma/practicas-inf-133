import requests
url = 'http://localhost:8000/graphql'

print("\nCrear nueva planta---------------\n")
query_crear_p = """
mutation {
    crearPlanta(nombre: "B", especie: "C", edad: 5, altura:1.3, frutos: true){
        planta {
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
}
"""

response_mutation = requests.post(url, json={'query': query_crear_p})
print(response_mutation.text)



print("\n- Listar plantas---------------\n")
query_lista = """
{
        plantas{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
}
"""
response = requests.post(url, json={'query': query_lista})
print(response.text)



print("\n- Buscar plantas de especie-----------\n")
query_lista_especie = """
{
        plantasPorEspecie(especie:"Rosa indica"){
            id
            nombre
        }
}
"""
response = requests.post(url, json={'query': query_lista_especie})
print(response.text)




print("\n- Buscar las plantas de frutos------\n")
query_frutos= """
{
    plantasPorFrutos{
        nombre
    }
}
"""
response = requests.post(url, json={'query': query_frutos})
print(response.text)




print("\n- Actualizar planta--------------\n")
query_modificar_p = """
mutation {
    modificarPlanta(id: 1, nombre: "NuevoN", especie: "NuevaE", edad: 10, altura: 2.5, frutos: true) {
        planta {
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
}
"""

responses = requests.post(url, json={'query': query_modificar_p})
print(responses.text)

query_eliminar = """
mutation {
        eliminarPlanta(id: 3) {
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""



print("\n- Eliminar una planta------------------\n")
response_mutation = requests.post(url, json={'query': query_eliminar})
print(response_mutation.text)




print("\n- Listar todas las plantas--------------\n")
response = requests.post(url, json={'query': query_lista})
print(response.text)