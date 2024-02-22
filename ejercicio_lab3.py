import csv
class Persona:
    def __init__(self, nombre, tipo_usuario, contrasena,controlador):
        self.nombre = nombre
        self.tipo_usuario = tipo_usuario
        self.contrasena = contrasena
        self.controlador = controlador
        

    def acceder_menu(self):

            while True:
                print("\n"*5)
                print("-"*50)
                print("Menú".center(50," "))
                print("-"*50)
                print("[1] Agregar dispositivo")
                print("[2] Eliminar dispositivo")
                print("[3] Agregar función a dispositivo")
                print("[4] Operar dispositivos")
                print("[5] Salir")
                opcion = int(input("Seleccione una opción: "))
                if opcion == 1:
                    if self.tipo_usuario == "admin":
                        self.controlador.agregar_dispositivo()

                    else:
                        print("No tiene permisos para realizar está acción")
                elif opcion == 2:
                    if self.tipo_usuario == "admin":
                        self.controlador.eliminar_dispositivo()
                    else:
                        print("No tiene permisos para realizar está acción")
                elif opcion == 3:
                    if self.tipo_usuario == "admin":
                        self.controlador.agregar_funcion_dispositivo()
                elif opcion == 4:
                    self.controlador.operar_dispositivos()
                                
                elif opcion == 5:
                    main()
                else:
                    print("Opción inválida")

    @classmethod
    def cargar_usuarios_desde_csv(cls, filename,controlador):
        usuarios = []
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                usuario = cls(row['nombre'], row['tipo_usuario'], row['contrasena'],controlador)
                usuarios.append(usuario)
        return usuarios

    def guardar_usuario_en_csv(self, usuarios):
        with open('usuarios.csv', 'a', newline='') as csvfile:
            fieldnames = ['nombre', 'tipo_usuario', 'contrasena']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            writer.writerow({'nombre': self.nombre, 'tipo_usuario': self.tipo_usuario, 'contrasena': self.contrasena})




class Dispositivo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.acciones = []

    def agregar_accion(self,accion):
            self.acciones.append(accion)

class Accion:
    def __init__(self, nombre,parametros=None):
        self.nombre= nombre
        self.parametros = parametros if parametros is not None else []

    def  agregar_parametro(self,parametro):
        self.parametros.append(parametro)
    

class ControladorDispositivo:
    def __init__(self):
        self.dispositivos = []
    def cargar_dispositivos(self):
        with open('dispositivos.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                dispositivo = Dispositivo(row['Nombre'])
                acciones = [Accion(accion) for accion in row['Acciones'].split(',')]
                for acc in acciones:
                    dispositivo.agregar_accion(acc)
                self.dispositivos.append(dispositivo)
    def agregar_dispositivo(self):
        print("\n"*5)
        print("-"*50)
        print("Agregar Dispositivo".center(50," "))
        print("-"*50)
        dispositivo = Dispositivo(input("Ingrese el nombre del dispositivo: "))
        self.dispositivos.append(dispositivo)
        self.guardar_dispositivos('dispositivos.csv') 

    def eliminar_dispositivo(self):
        print("\n"*5)
        print("-"*50)
        print("Eliminar dispositivo".center(50," "))
        print("-"*50)
        nombre_dispositivo = input("Ingrese el nombre del dispositivo a eliminar: ")
        for dispositivo in self.dispositivos:
            if dispositivo.nombre == nombre_dispositivo:
                self.dispositivos.remove(dispositivo)
                self.guardar_dispositivos('dispositivos.csv')
                return
            else:
                print("Dispositivo no encontrado")

    def agregar_funcion_dispositivo(self):
        print("\n"*5)
        print("-"*50)
        print("Agregar Función".center(50," "))
        print("-"*50)
        nombre_dispositivo = input("Ingrese el nombre del dispositivo al que desea agregar una función: ")
        dispositivo = None
        for d in self.dispositivos:
            if d.nombre == nombre_dispositivo:
                dispositivo = d
        
        if dispositivo:
            nombre_funcion = input("Ingrese el nombre de la función: ")
            parametros = input("Ingrese los parámetros de la función (separados por comas): ").split(",")
            funcion = Accion(nombre_funcion, parametros)
            dispositivo.agregar_accion(funcion)
            self.guardar_dispositivos('dispositivos.csv')
        else:
            print("Dispositivo no encontrado")

    def mostrar_dispositivos_y_acciones(self):
        for dispositivo in self.dispositivos:
            print("Nombre del dispositivo: "+dispositivo.nombre)
            print("Acciones:")
            for accion in dispositivo.acciones:
                print(accion.nombre)
            print()

    def operar_dispositivos(self):
        self.mostrar_dispositivos_y_acciones()
        dispositivo_elegido = input ("Ingrese el nombre del dispositivo a operar: ")
        accion_elegida = input("Ingrese la acción que desea realizar con este dispositivo: ")
        dispositivo = None
        for d in self.dispositivos:
            if d.nombre == dispositivo_elegido:
                dispositivo = d
        if dispositivo:
            accion = None
            for a in dispositivo.acciones:
                if a.nombre == accion_elegida:
                    accion = a
            if accion:
                print("Se va a realizar la acción: ", accion.nombre," en el dispositivo ",dispositivo.nombre)
            else:
                print("La acción: ",accion_elegida," no se encuentra registrada")
        else:
            print("El dispositivo ", dispositivo_elegido," no se encuentra registrado.")


    def mostrar_dispositivos_y_acciones(self):
        for dispositivo in self.dispositivos:
            print("Nombre: "+dispositivo.nombre)
            print("Acciones")
            for accion in dispositivo.acciones:
                print(accion.nombre)
            print()
    def guardar_dispositivos(self, archivo):
        with open(archivo, 'w', newline='') as csvfile:
            fieldnames = ['Nombre', 'Acciones']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for dispositivo in self.dispositivos:
                row = {'Nombre': dispositivo.nombre}
                acciones = [accion.nombre for accion in dispositivo.acciones]
                row['Acciones'] = ', '.join(acciones)
                writer.writerow(row)

def main():
    
    controlador = ControladorDispositivo()
    controlador.cargar_dispositivos()
    usuarios = Persona.cargar_usuarios_desde_csv('usuarios.csv',controlador)
    print(usuarios)
    while True:
        print("\n"*5)
        print("-"*50)
        print("Sistema de Control de Dispositivos Domésticos".center(50," "))
        print("-"*50)
        print("[I]Ingresar")
        print("[R]Registrar Usuario")
        print("[S]Salir")

      
        opcion=input(":>").upper()

        if opcion == "R":
            print("\n"*5)
            print("-"*50)
            print("Registro de usuario".center(50," "))
            print("-"*50)
            name=input("Nombre de Usuario: ")
            password=input("Contraseña: ")
            type=input("Tipo de Usuario (\"admin\",\"pac\"): ")

          
            if existe_usuario(name, usuarios):
                print("El usuario ya existe.")
   
            usuario = Persona(name, type, password,controlador)
            usuarios.append(usuario)
            print("Usuario registrado exitosamente.")
            usuario.guardar_usuario_en_csv(usuarios)

        elif opcion == "I":

            print("\n"*5)
            print("-"*50)
            print("Inicio de Sesión".center(50," "))
            print("-"*50)
            name=input("Nombre de Usuario: ")
            password=input("Contraseña: ")
            usuario = next((u for u in usuarios if u.nombre == name and u.contrasena == password), None)

            if usuario:
                usuario.acceder_menu()

            else:
                print("El usuario no existe o la contraseña es incorrecta.")
        elif opcion == "S":
            exit()

        else:
            print("Opción invalida")
            main()

def existe_usuario(name, usuarios):
    return next((u for u in usuarios if u.nombre == name), None) is not None  
usuarios = []
main()

