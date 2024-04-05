from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from urllib.parse import urlparse, parse_qs

patients = {}
class Patient:
    def __init__(self):
        self.nombre = None
        self.apellido = None
        self.edad = 0
        self.genero = None
        self.diagnostico = None
        self.doctor = None  # Agregar el atributo doctor

    def __str__(self):
        return f"Nombre: {self.nombre}, Apellido: {self.apellido}, Edad: {self.edad}, Género: {self.genero}, Diagnóstico: {self.diagnostico}, Doctor: {self.doctor}"

class PatientBuilder:
    def __init__(self):
        self.patient = Patient()
        
    def set_nombre(self, nombre):
        self.patient.nombre = nombre
    
    def set_apellido(self, apellido):
        self.patient.apellido = apellido
        
    def set_edad(self, edad):
        self.patient.edad = edad
        
    def set_genero(self, genero):
        self.patient.genero = genero
        
    def set_diagnostico(self, diagnostico):
        self.patient.diagnostico = diagnostico
    
    def set_doctor(self, doctor):  # Agregar el método set_doctor
        self.patient.doctor = doctor
    
    def get_patient(self):
        return self.patient
    
class Hospital:
    def __init__(self, builder):
        self.builder = builder
        
    def create_patient(self, nombre, apellido, edad, genero, diagnostico, doctor):
        self.builder.set_nombre(nombre)
        self.builder.set_apellido(apellido)
        self.builder.set_edad(edad)
        self.builder.set_genero(genero)
        self.builder.set_diagnostico(diagnostico)
        self.builder.set_doctor(doctor)  # Configurar el doctor en el builder
        return self.builder.get_patient()

class PatientService(BaseHTTPRequestHandler):
    def __init__(self):
        self.builder = PatientBuilder()
        self.hospital = Hospital(self.builder)
        
    
    def handle_post_request(self, post_data):
        nombre = post_data.get("nombre", None)
        apellido = post_data.get("apellido", None)
        edad = post_data.get("edad", None)
        genero = post_data.get("genero", None)
        diagnostico = post_data.get("diagnostico", None)
        doctor = post_data.get("doctor", None)  # Obtener el valor del doctor del post_data
        
        patient = self.hospital.create_patient(nombre, apellido, edad, genero, diagnostico, doctor)
        patients[len(patients) + 1] = patient
        return patient
    
    def read_patients(self):
        return {index: patient.__dict__ for index, patient in patients.items()}
    
    def find_patient_by_CI(self, CI):
        for i, patient in patients.items() :
            if i == CI:
                return patient
            
    def delete_patient(self, index):
        if index in patients:
            return patients.pop(index)
        else:
            return None

    def find_by_doctor(self, doctor):
        patientD = []
        for i, patient in patients.items():
            if patient.doctor == doctor:
                patientD.append(patient.__dict__)  # Agregar el diccionario que representa al paciente
        return patientD

    
    def find_by_diagnostic(self, diagnostic):
        patientD = []
        for i, patient in patients.items():
            if patient.diagnostico == diagnostic:
                patientD.append(patient.__dict__)  # Agregar el diccionario que representa al paciente
        return patientD
    def put_patient(self, index, data):
        if index in patients:
            patient = patients[index]
            nombre = data.get("nombre", None)
            apellido = data.get("apellido", None)
            edad = data.get("edad", None)
            genero = data.get("genero", None)
            diagnostico = data.get("diagnostico", None)
            doctor = data.get("doctor", None)
            
            if nombre:
                patient.nombre = nombre
            if apellido:
                patient.apellido = apellido
            if edad:
                patient.edad = edad
            if genero:
                patient.genero = genero
            if diagnostico:
                patient.diagnostico = diagnostico
            if doctor:
                patient.doctor = doctor
            
            return patient
        else:
            return None




class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers['Content-Length'])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

class PatientHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = PatientService()
        super().__init__(*args, **kwargs)
        
        
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if self.path == "/patients":
            response_data = self.controller.read_patients()
            HTTPDataHandler.handle_response(self, 200, response_data)
        elif parsed_path.path == "/patients":
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                patient_filtred = self.controller.find_by_diagnostic(diagnostico)
                print(patient_filtred)
                if patient_filtred: HTTPDataHandler.handle_response(self, 200, patient_filtred)
                else: HTTPDataHandler.handle_response(self, 404, {"Error":"patient not found"})
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                patient_filtred = self.controller.find_by_doctor(doctor)
                if patient_filtred: HTTPDataHandler.handle_response(self, 200, patient_filtred)
                else: HTTPDataHandler.handle_response(self, 404, {"Error":"patient not found"})
            else:
                HTTPDataHandler.handle_response(self, 404, patients)
            
        elif self.path.startswith("/patients/"):
            index = int(self.path.split("/")[2])
            find_patient = self.controller.find_patient_by_CI(index)
            if find_patient:
                HTTPDataHandler.handle_response(self, 200, find_patient.__dict__)
            else: 
                HTTPDataHandler.handle_response(self, 404, {"Error": "Patient not found"})

        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


    def do_POST(self):
        if self.path == '/patients':
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.handle_post_request(data)
            
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
    def do_DELETE(self):
        if self.path.startswith("/patients/"):
            index = int(self.path.split("/")[2])
            delete_patient = self.controller.delete_patient(index)
            if delete_patient:
                HTTPDataHandler.handle_response(self, 200, delete_patient.__dict__)
            else: HTTPDataHandler.handle_response(self, 404, {"Error":"No se encontro a un paciente con ese CI"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
    def do_PUT(self):
        if self.path.startswith("/patients/"):
            index = int(self.path.split("/")[2])  # Usamos 'index' en lugar de 'CI'
            data = HTTPDataHandler.handle_reader(self)
            response_put = self.controller.put_patient(index, data)  # Pasamos 'index' a 'put_patient'
            if response_put:
                HTTPDataHandler.handle_response(self, 200, response_put.__dict__)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

            
def run(server_class=HTTPServer, handler_class=PatientHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()