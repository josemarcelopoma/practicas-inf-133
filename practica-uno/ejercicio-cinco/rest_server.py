from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# parametros query
from urllib.parse import parse_qs, urlparse
animales= []
# 1 creamos el RESTrequesthandler

class RESTRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))    
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode('utf-8'))
        return data
    def find_animal_by_id(self,id):
        return next((animal for animal in animales if animal["id"] == id), None,)
    def do_POST(self):
        if self.path == "/animales":
            data = self.read_data()
            data["id"] = len(animales)+1
            animales.append(data)
            self.response_handler(201, animales)
    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            index = int(self.path.split("/")[-1])
            Eliminar_animal=None
            for i, animal in enumerate(animales):
                if animal["id"] ==index:
                    Eliminar_animal = animales.pop(i)
            if Eliminar_animal: self.response_handler(200, Eliminar_animal)
            else: self.response_handler(404, {"Message":"ningun animal con el id"})
        else: self.response_handler(404, {"Error":"ruta no existente"})
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if parsed_path.path == "/animales":
            if "especie" in query_params:
                especie = query_params["especie"][0]
                animal_filtrado = [
                    animal for animal in animales if animal["especie"] == especie
                ]
                if animal_filtrado:
                    self.response_handler(200, animal_filtrado)
                else: self.response_handler(404, {"Message":"especie de animal no encontrado"})
            elif "genero" in query_params:
                genero = query_params["genero"][0]
                animal_filtrado = [
                    animal for animal in animales if animal["genero"] == genero
                ]
                if animal_filtrado:
                    self.response_handler(200, animal_filtrado)
                else: self.response_handler(404, {"Message":"genero de animal no encontrado"})
                
            else: self.response_handler(200,animales)

        elif self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animal = self.find_animal_by_id(id)
            if animal:
                self.response_handler(200, animal)
            else: self.response_handler(404, {"Mssage":"ningun animal con ID"})
        else:
            self.response_handler(404, {"Error":"ruta no existente"})
            
    def do_PUT(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animal = self.find_animal_by_id(id)
            data = self.read_data()
            if animal:
                animal.update(data)
                self.response_handler(200, animal)
            else:
                self.response_handler(404, {"Error": "No encontrado"})
        else:
            self.response_handler(404, {"Error": "La Ruta no existe"})



def run_server(port=8000):

    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()