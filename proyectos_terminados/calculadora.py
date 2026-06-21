print("=============== CALCULADORA ===============")

class Calculadora:
    def pedir_numero(self):
        while True:
            try:
                num = float(input("Ingresa un número: "))
                return num
            except ValueError:
                print("Error: valor ingresado no numerico")
            except KeyboardInterrupt:
                respuesta = self.salir()
                if respuesta == True: return "ADIOS"
                
                else:
                    print(respuesta)
    
    def salir(self):
        while True:
            try:
                pregunta = input("\n¿Deseas salir al menu principal? (Sí/No): ").strip().lower()
                if pregunta in ["sí", "si"]:
                    return True
                elif pregunta == "no": 
                    return f"Bien, continuemos."
                else: 
                    print("Por favor, sólo responde 'sí' o 'no'")
            except KeyboardInterrupt:
                print("\nEjecución interrumpida por el usuario")
                return True
    
                
    def operacion(self, signo):
        num1 = self.pedir_numero()
        result = num1
        if num1 == "ADIOS":
            print("Bien, hagamos otra operación")
            return None

        flag = False
        while True:
            while True:
                num = self.pedir_numero()
                if num == "ADIOS" and flag: # flag == True
                    return result
                elif num == "ADIOS":
                    print("Bien, hagamos otra operación")
                    return None
                elif num == 0 and signo == "/":
                    print("Error: ¡El denominador no debe ser igual a cero!")
                else:
                    flag = True
                    break
            
            #Tipo de operador aritmetico
            if signo == "+":
                result += num
            elif signo == "-":
                result -= num
            elif signo == "*":
                result *= num
            elif signo == "/":
                result /= num
            elif signo == "**":
                result **= num

            while flag:
                try:    
                    pregunta = input("¿Deseas agregar otro numero? (Sí/No): ").strip().lower()  
                    if pregunta in ["sí", "si"]:
                        break
                    elif pregunta == "no": return result
                    
                    else:
                        print("Por favor, sólo responde 'sí' o 'no'")
                except KeyboardInterrupt:
                    print("\nInterrumpiste la ejecución")
                    return result
        
objeto = Calculadora()

OPCIONES = {1: "+", 2: "-", 3: "*", 4: "/", 5: "**"}     
bucle_principal = True
while bucle_principal:
    print("""Elige una operación:
1. Sumar
2. Restar
3. Multiplicar
4. Dividir
5. Elevar (potencia)
6. Salir""")
    
    while True:
        try:
            opcion = int(input(">>>: "))
            if opcion == 6:
                print("\nGracias por usar mi calculadora, adiós :)")
                bucle_principal = False
                break
            elif opcion in [1, 2, 3, 4, 5]:
                resultado = objeto.operacion(OPCIONES[opcion])
                break
            else:
                print("Opción elegida fuera de rango, sólo es del 1 al 6")
        except ValueError:
            print("Error: valor ingresado no numerico :(")
        except KeyboardInterrupt:
            print("\nAcción interumpida por el usuario. ¡Hasta luego!")
            opcion = 0
            bucle_principal = False
            break
    
    if opcion != 0 and resultado != None:
        print(f"\nEl resultado de la operación es: {resultado:.2f}\n")