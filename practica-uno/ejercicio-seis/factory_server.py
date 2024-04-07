from http.server import HTTPServer, BaseHTTPRequestHandler
import json
animales = {}
class Animal_crear:
    def __init__(self, id_animal, nombre, especies, Genero, Edada, Altura):
        self.id_animal = id_animal
        self.nombre = nombre
        self.especies = especies
        self.Genero = Genero
        self.Edada = Edada
        self.Altura = Altura
    def __str__(self):
        return f"ID: {self.id_animal}, Name: {self.nombre}, Species: {self.especies}, Gender: {self.Genero}, Age: {self.Edada}, Weight: {self.Altura}"

class crear_mamifero(Animal_crear):
    def __init__(self, id_animal, nombre, especies, Genero, Edada, Altura):
        super().__init__(id_animal, nombre, especies, Genero, Edada, Altura)
class crear_ave(Animal_crear):
    def __init__(self, id_animal, nombre, especies, Genero, Edada, Altura):
        super().__init__(id_animal, nombre, especies, Genero, Edada, Altura)
class crear_reptil(Animal_crear):
    def __init__(self, id_animal, nombre, especies, Genero, Edada, Altura):
        super().__init__(id_animal, nombre, especies, Genero, Edada, Altura)
class crear_anfibio(Animal_crear):
    def __init__(self, id_animal, nombre, especies, Genero, Edada, Altura):
        super().__init__(id_animal, nombre, especies, Genero, Edada, Altura)
class crear_pez(Animal_crear):
    def __init__(self, id_animal, nombre, especies, Genero, Edada, Altura):
        super().__init__(id_animal, nombre, especies, Genero, Edada, Altura)

        
class Animal_factory:
    @staticmethod
    def crear_Animal_(animal_type, id_animal, nombre, especies, Genero, Edada, Altura):
        if animal_type == "mamifero":
            return crear_mamifero(id_animal, nombre, especies, Genero, Edada, Altura)
        elif animal_type == "ave":
            return crear_ave(id_animal, nombre, especies, Genero, Edada, Altura)
        elif animal_type == "reptil":
            return crear_reptil(id_animal, nombre, especies, Genero, Edada, Altura)
        elif animal_type == "anfibio":
            return crear_anfibio(id_animal, nombre, especies, Genero, Edada, Altura)
        elif animal_type == "pez":
            return crear_pez(id_animal, nombre, especies, Genero, Edada, Altura)
        else:
            raise ValueError("animal no valido")



class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

class servicios_animal:
    def __init__(self):
        self.factory = Animal_factory()
        
    def Añadir_animal(self, data):
        if not animales:
            id_animal = 1
        else:
            id_animal = max(animales.keys()) + 1
        
        animal = self.factory.crear_Animal_(data["animal_type"], id_animal, data["nombre"], data["especies"], data["Genero"], data["Edada"], data["Altura"])
        animales[len(animales)] = animal
        
        return animal
    
    def __init__(self):
        self.factory = Animal_factory()
        
    def actualizar_animal(self, id_animal, data):
        if id_animal in animales:
            animal = animales[id_animal]
            nombre = data.get("nombre", None)
            especies = data.get("especies", None)
            Genero = data.get("Genero", None)
            Edada = data.get("Edada", None)
            Altura = data.get("Altura", None)
            if nombre:

                animal.nombre = nombre

            if especies:

                animal.especies = especies

            if Genero:

                animal.Genero = Genero

            if Edada:

                animal.Edada = Edada

            if Altura:

                animal.Altura = Altura

            return animal
            
        else:
            return None
    
    def list_animal(self):
        return {index: animal.__dict__ for index, animal in animales.items()}
        
    def delete_animal(self,id_animal):
        if id_animal in animales:
            an = animales.pop(id_animal)
            return an
        else:
            return None
        
        
class ZoologicoRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.animal_service = servicios_animal()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == "/animales":
            response_data = self.animal_service.list_animal()
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Message": "lista vacía"})

    def do_POST(self):
        if self.path == "/animales":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.animal_service.Añadir_animal(data)
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "no encontrado"}
            )
    def do_PUT(self):
        if self.path.startswith("/animales/"):
            id_animal = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.animal_service.actualizar_animal(id_animal, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Animal_crear no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "no encontrado"}
            )
            
    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            id_animal = int(self.path.split("/")[-1])
            response_data = self.animal_service.delete_animal(id_animal)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Animal_crear no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "ruta no encontrada"}
            )
def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, ZoologicoRequestHandler)
        print("Iniciando servidor HTTP 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando server HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()