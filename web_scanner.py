import requests
import time

class EscanerWeb:
    def __init__(self, url, file):
        if not url.endswith("/"):
            url += "/"
        self.url = url
        self.archivo = file
        self.lista = []
    
    def cargar_archivo_txt(self):
        with open(self.archivo, "a+", encoding="utf-8") as archivo:
            archivo.write(f"\n===== INICIO DEL REPORTE ({time.strftime('%d-%m-%Y %H:%M:%S')}) =====\n")
        
    def escanear_cabeceras(self):
        try:
            respuesta = requests.get(self.url)
            self.lista.clear()
            self.guardar_reporte("\n===== Cabeceras =====:")
            for clave, valor in respuesta.headers.items():
                print(f"{clave}: {valor}")
                self.guardar_reporte(f"{clave}: {valor}")
            print("\n[v] Cabeceras escaneadas y cargadas a la memoria.")
        except requests.exceptions.ConnectionError:
            print("Error: No se pudo conectar al servidor para obtener las cabeceras.")
                
    def fuzzing_directorios(self):
        directorios = ["admin", "login", "uploads", "robots.txt", "backup"]
        
        try:
            base_respuesta = requests.get(self.url)
            longitud_index = len(base_respuesta.text)
        except requests.exceptions.ConnectionError:
            print("Error crítico: No se pudo establecer la conexión base con el servidor.")
            return

        self.guardar_reporte("\n===== DIRECCIONES DETECTADAS =====")
        print(f"\nIniciando fuzzing en {self.url}... (Presiona Ctrl+C para detener y guardar)")

        for directorio in directorios:
            try:
                respuesta = requests.get(f"{self.url}{directorio}")
                
                if respuesta.status_code == 200:
                    if len(respuesta.text) == longitud_index:
                        pass
                    else:
                        resultado = f"[+] Encontrado: /{directorio} (Código 200)"
                        print(resultado)
                        self.guardar_reporte(resultado)
                elif respuesta.status_code == 403:
                    resultado = f"[-] Encontrado, pero protegido: /{directorio} (Código 403)"
                    print(resultado)
                    self.guardar_reporte(resultado)
                elif respuesta.status_code == 404:
                    pass
                elif respuesta.status_code == 500:
                    print(f"[!] Servidor devolvió error 500 en: /{directorio}")
                    
            except KeyboardInterrupt:
                print("\n\n[!] Escaneo interrumpido por el usuario.")
                answer = self.salir()
                if answer == "ADIOS":
                    print("Guardando progreso acumulado en el archivo...")
                    self.guardar_archivo()
                    return
                elif answer == "SALIR":
                    print("Saliendo sin guardar cambios de este escaneo.")
                    return
                print("Continuando con el escaneo de directorios...")
        
        self.guardar_archivo()
        print("\n[v] Fuzzing completado. Resultados respaldados en el archivo.")
                    
    def guardar_reporte(self, resultado):
        if resultado not in self.lista:
            self.lista.append(resultado)

    def guardar_archivo(self):
        with open(self.archivo, "a", encoding="utf-8") as archivo:
            for linea in self.lista:
                archivo.write(f"{linea}\n")
        self.lista.clear()

    def salir(self):
        while True:
            pregunta = input("¿Deseas guardar lo que encontraste antes de ir al menú? (Sí/No/Sólo Salir): ").strip().lower()
            if pregunta in ["sí", "si"]: return "ADIOS"
            if pregunta in ["solo salir", "sólo salir", "no"]: return "SALIR"
            print("Por favor, responde 'sí', 'no' o 'sólo salir'")

objeto = EscanerWeb("https://sentinelcareai.pages.dev/", "reporte.txt")
objeto.cargar_archivo_txt()

while True:
    print("\nElige una opción:\n1. Mostrar los headers\n2. Escaneo de directorios (Fuzzing)\n3. Guardar reporte actual en disco\n4. Salir\n")
    try:
        op = int(input(">>>: "))
        if op == 1: 
            objeto.escanear_cabeceras()
        elif op == 2: 
            objeto.fuzzing_directorios()
        elif op == 3: 
            objeto.guardar_archivo()
            print("Guardando archivo...")
            time.sleep(2)
            print("[v] Archivo guardado de forma segura.")
        elif op == 4: 
            print("¡Hasta luego, inspector!")
            break
        else:
            print("Opción no existente.")
    except ValueError:
        print("Error: El valor ingresado debe ser numérico.")
    except KeyboardInterrupt:
        print("\n\nEjecución interrumpida de golpe. ¡Hasta luego!")
        break