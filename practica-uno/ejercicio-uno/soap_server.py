from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher , SOAPHandler





def sumarnumero(num1,num2):
    return "suma es:".format(num1+num2)
    
def restar_numeros(num1, num2):
    return "La resta es: {}".format(num1-num2)

def miltiplicar_numeros(num1, num2):
    return "La multiplicacion es: {}".format(num1*num2)

def dividir_numeros(num1, num2):
    if num2 == 0: return "La division no es posible porque el divisor es 0"
    return "La division es: {}".format(num1/num2)


dispatcher = SoapDispatcher(
    "ejemplo-soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)
dispatcher.register_function(
    "sumardosnumero",
    sumarnumero,
    returns={"suma":str},
    args={"num1":int ,"num2":int},
)
dispatcher.register_function(
    "RestaDosNumeros",
    restar_numeros,
    returns = {"resta": str},
    args = {"num1": int, "num2": int}
)

dispatcher.register_function(
    "MultiplicaDosNumeros",
    miltiplicar_numeros,
    returns = {"multiplicacion": str},
    args ={"num1": int, "num2": int}
)
dispatcher.register_function(
    "DivideDosNumeros",
    dividir_numeros,
    returns = {"divicion": str},
    args ={"num1": int, "num2": int}
)

server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()