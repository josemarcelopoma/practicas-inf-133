from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs
pacientes = []
class pacientesServicios:
    @staticmethod
    def encontrar_pac(CI):
        return next(
            (paciente for paciente in pacientes if paciente["CI"] == CI),
            None,
        )
    @staticmethod
    def enocntrar_paciente_doc(name):
        doctors = [paciente for paciente in pacientes if paciente["doctor"] == name]
        return doctors
        
    @staticmethod
    def encontrar_paciente_diag(name):
        diagnostics = [paciente for paciente in pacientes if paciente["diagnostico"] == name]
        return diagnostics
    
    @staticmethod
    def añadir_pac(data):
        if not pacientes: data["CI"] = 1
        else: data["CI"] = max(pacientes, key=lambda x: x["CI"])["CI"]+1
        pacientes.append(data)
        return data
    
    @staticmethod
    def actualizar_pac(CI,data):
        paciente = pacientesServicios.encontrar_pac(CI)
        if paciente: 
            paciente.update(data)
            return paciente
        else: 
            return None
        
    @staticmethod
    def borrar_pac(CI):
        paciente = pacientesServicios.encontrar_pac(CI)
        if paciente:
            pacientes.remove(paciente)
            return paciente
        else: return None
    




class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if parsed_path.path == "/pacientes":
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                patient_filtred = pacientesServicios.encontrar_paciente_diag(
                    diagnostico
                )
                if patient_filtred != []: HTTPResponseHandler.handle_response(self, 200, patient_filtred)
                else: HTTPResponseHandler.handle_response(self, 204, [])
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                patient_filtred = pacientesServicios.enocntrar_paciente_doc(
                    doctor
                )
                if patient_filtred != []: HTTPResponseHandler.handle_response(self, 200, patient_filtred)
                else:  HTTPResponseHandler.handle_response(self, 204, [])
            else:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
        elif self.path.startswith("/pacientes/"):
            id = int(self.path.split("/")[-1])
            paciente = pacientesServicios.encontrar_pac(id)
            if paciente: HTTPResponseHandler.handle_response(self, 200, [paciente])
            else: HTTPResponseHandler.handle_response(self, 204, {"Error":"paciente not found"})
        else: HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            pacientes = pacientesServicios.añadir_pac(data)
            HTTPResponseHandler.handle_response(self, 201, pacientes)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )
    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            CI = int(self.path.split("/")[-1])
            data = self.read_data()
            pacientes = pacientesServicios.actualizar_pac(CI, data)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Estudiante no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            CI = int(self.path.split("/")[-1])
            paciente = pacientesServicios.borrar_pac(CI)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, [paciente])
            else:
                HTTPResponseHandler.handle_response(self, 404, "Patient not found")
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data






def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("--Apagando servidor--")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()