from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

Sum = lambda a,b: a+b

Rest = lambda a,b: a-b

Multi = lambda a,b: a*b

Div = lambda a,b: "No se puede dividir por cero" if b==0 else a/b

dispatcher = SoapDispatcher(
    "Dispatcher-pract",
    location="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)

dispatcher.register_function(
    "Suma",
    Sum,
    returns={"suma": str},
    args={"a": int, "b": int},
)

dispatcher.register_function(
    "Resta",
    Rest,
    returns = {"resta": str},
    args = {"a": int, "b": int}
)
dispatcher.register_function(
    "Multiplicacion",
    Multi,
    returns = {"multiplicacion": str},
    args ={"a": int, "b": int}
)
dispatcher.register_function(
    "Divicion",
    Div,
    returns = {"divicion": str},
    args ={"a": int, "b": int}
)
server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()