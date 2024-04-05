from zeep import Client
client = Client("http://localhost:8000/")

result = client.service.Suma(a=3, b=3)
print(result)
result = client.service.Resta(a=3, b=3)
print(result)
result = client.service.Multiplicacion(a=3, b=3)
print(result)
result = client.service.Divicion(a=3, b=0)
print(result)