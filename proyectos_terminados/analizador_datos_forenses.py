import time

class AnalizadorForense:
    def __init__(self, file):
        self.archivo = file
        self.conteo_ips = {}
        self.fuerza_bruta = {}
        self.escaneo_rutas = {}
        
    def analizar_archivo(self):
        try:
            with open(self.archivo, "r") as file:
                print("Iniciando el analisis del archivo....")
                time.sleep(2)
                for linea in file:
                    line = linea.split(" ")
                    ip = line[0]
                    codigo = line[7]
                    if ip not in self.conteo_ips: 
                        self.conteo_ips[ip] = 1
                    elif ip in self.conteo_ips:
                       self.conteo_ips[ip] += 1
                    
                    if codigo == "401":
                        if ip not in self.fuerza_bruta: self.fuerza_bruta[ip] = 1
                        else: self.fuerza_bruta[ip] += 1
                    elif codigo == "404":
                        if ip not in self.escaneo_rutas: self.escaneo_rutas[ip] = 1
                        else: self.escaneo_rutas[ip] += 1
                print("\n[v] IP´s guardadas correctamente :)\n") 
        except KeyboardInterrupt: 
            respuesta = self.salir()
            if respuesta == "SALIR": return
        except FileNotFoundError:
            print("Archivo no existente")

    def detectar_amenazas(self):
        try:
            if self.conteo_ips == {}:
                print("\nLa lista está vacía :(\n")
            else:
                print("Iniciando escaneo de amenazas....")
                time.sleep(2)
                print("=== REPORTE DE AMENAZAS DETECTADAS ===")
                for ip in self.conteo_ips:
                    if self.conteo_ips[ip] > 4:
                        if ip in self.escaneo_rutas:
                            print(f"[!] SOSPECHA DE ESCANEO (FUZZING): La IP {ip}, buscó {self.escaneo_rutas[ip]} páginas inexistentes.")
                        if ip in  self.fuerza_bruta:
                            print(f"[!] SOSPECHA DE FUERZA BRUTA: La IP {ip}, tiene {self.fuerza_bruta[ip]} intentos fallidos de login.")
                        
                print("\n[v] Detector de amenazas finalizado :)\n")
        except KeyboardInterrupt:
            respuesta = self.salir()
            if respuesta == "SALIR": return
    
    def salir(self):
        while True:
            pregunta = input("\n¿Deseas salir? (Sí/No): ").strip().lower()
            if pregunta in ["sí", "si"]: return "SALIR"
            elif pregunta == "no": return "CONTINUAR"
            print("Por favor, sólo escribe 'sí' o 'no'")
    
    
archivo_log = AnalizadorForense("servidor.log")

while True:
    print("Elige una opción: \n1. Analizar Logs \n2. Detectar Amenazas")
    try:
        op = input(">>>: ").strip().lower()
        if op in ["1", "analizar logs"]:
            archivo_log.analizar_archivo()
        elif op in ["2", "detectar amenazas"]:
            archivo_log.detectar_amenazas()
        else:
            print("Opción no existente")
    except KeyboardInterrupt:
        print("\nEjecución terminada por el usuario. ¡Hasta luego!")
        break
