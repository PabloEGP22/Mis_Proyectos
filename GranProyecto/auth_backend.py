import hashlib, json
from GranProyecto.validador import validador_contraseñas
from GranProyecto.validador import validador_usuarios

class AuthBackend:
    def __init__(self):
        self.base_datos = {}
        self.intentos_fallidos = {}
        self.cargar_archivo()
    
    def guardar_archivo(self):
        try:
            # Abrimos el archivo en modo escritura ('w')
            with open("usuarios.json", "w", encoding="utf-8") as archivo:
                # json.dump toma tu diccionario y lo escribe estructurado en el archivo
                json.dump(self.base_datos, archivo, indent=4)
            print("[v] Base de datos sincronizada en disco duro con éxito.")
        except Exception as error:
            print(f"Error al guardar el archivo: {error}")

    def cargar_archivo(self):
        try:
            # Abrimos en modo lectura ('r')
            with open("usuarios.json", "r", encoding="utf-8") as archivo:
                # json.load lee el archivo y lo transforma de vuelta en un diccionario de Python
                self.base_datos = json.load(archivo)
            print("[v] Datos de usuarios cargados correctamente desde el disco.")
        except FileNotFoundError:
            # Si el archivo no existe aún (primera ejecución), dejamos el diccionario vacío
            self.base_datos = {}
            
    def registrar_usuario(self, usuario, password):
        hash_objeto = hashlib.sha256(password.encode())
        hash_resultado = hash_objeto.hexdigest() 
        self.base_datos[usuario] = hash_resultado
    
    def login_usuario(self, usuario, password):
        if usuario not in self.base_datos:
            return "Usuario no encontrado"

        if usuario in self.intentos_fallidos and self.intentos_fallidos[usuario] >= 3:
            return "Acceso bloqueado: Has alcanzado el límite de 3 intentos fallidos."

        hash_objeto = hashlib.sha256(password.encode())
        hash_resultado = hash_objeto.hexdigest() 
        
        if hash_resultado == self.base_datos[usuario]:
            if usuario in self.intentos_fallidos:
                self.intentos_fallidos[usuario] = 0
            print("Acceso concedido")
            return True
        else:
            if usuario not in self.intentos_fallidos:
                self.intentos_fallidos[usuario] = 1
            else:
                self.intentos_fallidos[usuario] += 1
                
            intentos_restantes = 3 - self.intentos_fallidos[usuario]
            if intentos_restantes <= 0:
                return "Contraseña Incorrecta. ¡ATENCIÓN: Tu cuenta ha sido bloqueada por seguridad!"
            return f"Contraseña Incorrecta. Te quedan {intentos_restantes} intentos."
    
# objeto = AuthBackend()


# while True:
#     print("Elige una opción: \n1. Resgistrarme \n2. Iniciar Sesión \n3. Salir")
#     try:
#         op = input(">>>: ").strip()
#         if op in ["1", "resgistrarme"]:
#             while True:
#                 user = input("Ingresa un usuario: ").strip()
#                 retorno = validador_usuarios(user, objeto.base_datos)
#                 if retorno == True:
#                     break
                
#             while True:
#                 password = input("Ingresa una contraseña: ").strip()
#                 retorno = validador_contraseñas(password)
#                 if retorno == True:
#                     password_confirmation = input("Ingresa nuevamente la contraseña contraseña: ").strip()
#                     if password_confirmation == password:
#                         objeto.registrar_usuario(user, password)
#                         objeto.guardar_archivo()
#                         print("Cuenta creada con exito :)")
#                         break
#                     else:
#                         print("Las contraseñas no coinciden. Vuelve a intentarlo.")
#                 else:
#                     print(retorno)
#         elif op in ["2", "iniciar sesion", "iniciar sesión"]:
#             while True:
#                 usuario = input("Ingresa tu usuario: ").strip()
#                 contraseña = input("Ingresa tu contraseña: ").strip()
#                 retorno = objeto.login_usuario(usuario, contraseña)
#                 if retorno == True:
#                     break
#                 else:
#                     if "bloquead" in retorno:
#                         break
#         elif op in ["3", "salir"]:
#             print("¡Hasta luego!")
#             break
#         else:
#             print("Opción no existente")
#     except KeyboardInterrupt:
#         print("\nEjecución interrumpida por el usuario")
#         break
#     except Exception as error:
#         print(f"Error Inesperado: {error}")
