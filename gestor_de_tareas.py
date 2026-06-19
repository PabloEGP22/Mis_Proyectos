class Gestor:
    def __init__(self):
        self.tareas = []
        
    def agregar(self):
        while True:
            try:
                nombre = input("Ingresa el nombre de la tarea: ").strip().capitalize()
                if f"[] {nombre}" in self.tareas or f"[X] {nombre}" in self.tareas:
                    print("Tarea ya existente")
                else:
                    self.tareas.append(f"[] {nombre}")
                    print("¡Tarea agregada correctamente!\n")
                return
            except KeyboardInterrupt:
                respuesta = self.salir()
                if respuesta == "ADIOS": return
                print(respuesta)
    
    def mostrar(self):
        if self.tareas == []:
            print("No hay tareas para mostrar")
        else:
            for i, tarea in enumerate(self.tareas):
                print(f"{i+1}. {tarea}")
        
    def check(self):
        cont = 0 # Siempre que llame a la funcion cont empezara en 0
        for tarea in self.tareas:
            if "[]" in tarea:
                cont += 1
                
        while True:  
            if cont == 0:
                print("Todas las tareas han sido completadas :)")
                return
            else:
                try:
                    self.mostrar()
                    indice = int(input("Ingresa el indice de la tarea a marcar: "))
                    if 0 < indice <= len(self.tareas):
                        indice -= 1
                        if "[]" in self.tareas[indice]:
                            self.tareas[indice] = self.tareas[indice].replace("[]", "[X]")
                        else:
                            print("Tarea ya completada")
                        return
                    else:
                        print("Indice no existente")
                except ValueError:
                    print("Error: valor ingresado no numerico")
                except KeyboardInterrupt:
                    respuesta = self.salir()
                    if respuesta == "ADIOS": return
                    print(respuesta)
    
    def eliminar(self):
        if self.tareas == []:
            print("No hay tareas para eliminar :)")
        else:
            while True:
                try:
                    self.mostrar()
                    indice = int(input("Ingresa el indice de la tarea a eliminar: "))
                    if 0 < indice <= len(self.tareas):
                        indice -= 1
                        if "[X]" in self.tareas[indice]:
                            self.tareas.pop(indice)
                            print("Tarea eliminada correctamente")
                            return
                        elif "[]" in self.tareas[indice]:
                            print("Tarea aún no completada") 
                            while True:
                                pregunta = input("¿Deseas eliminarla aunque aún no está completada? (Sí/No): ").strip().lower()
                                if pregunta in ["sí", "si"]:
                                    self.tareas.pop(indice)
                                    print("Tarea eliminada correctamente")
                                    return
                                elif pregunta == "no":
                                    print("Bien, sigamos...")
                                    return
                                else:
                                    print("Por favor, sólo responde 'sí' o 'no'")
                        else:
                            print("Tarea no encontrada, verifica si está bien escrita")
                    else:
                        print("Indice no existente")
                except ValueError:
                    print("Error: valor ingresado no numerico")
                except KeyboardInterrupt:
                    respuesta = self.salir()
                    if respuesta == "ADIOS": return
                    print(respuesta)
            
    def salir(self):
        while True:
            try:
                pregunta = input("\n¿Deseas salir? (Sí/No): ").strip().lower()
                if pregunta in ["si", "sí"]:
                    print("Hagamos otra cosa...")
                    return "ADIOS"
                elif pregunta == "no": return "Bien, continuemos"
                else:
                    print("Por favor, sólo responde 'sí' o 'no'")
            except KeyboardInterrupt:
                print("\n¡Ejecución terminada, adiós!")
                return "ADIOS"
        
    
objeto = Gestor()

# ======== BUCLE PRINCIPAL ========
bucle_principal = True
while bucle_principal:
    print("Elige una opción: \n1. Agregar \n2. Mostrar tareas \n3. Marcar tarea complatada \n4. Eliminar \n5. Salir")
    
    while True:
        try:
            opcion = int(input(">>>: "))
            if opcion == 5:
                print("¡Hasta luego!")
                bucle_principal = False
            elif opcion == 1: objeto.agregar()
            elif opcion == 2: objeto.mostrar()
            elif opcion == 3: objeto.check()
            elif opcion == 4: objeto.eliminar()
            else: print("Opcion no existente")
            break
        except ValueError: 
            print("Error: valor ingresado no numerico")
        except KeyboardInterrupt:
            print("\nEjecución interrumpida por el usuario")
            bucle_principal = False
            break
