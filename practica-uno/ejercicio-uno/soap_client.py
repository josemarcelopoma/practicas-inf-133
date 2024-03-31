from zeep import Client

client = Client('http://localhost:8000')

result = client.service.Saludar(nombre="Tatiana")
print(result)

resultado1 = client.service.sumardosnumero(num1 =1,num2 =1)
print(resultado1)



resultado = client.service.RestaDosNumeros(num1=1, num2=1)

print(resultado)

resultado = client.service.MultiplicaDosNumeros(num1=1, num2=1)

print(resultado)


resultado = client.service.DivideDosNumeros(num1=1, num2=0)

print(resultado)