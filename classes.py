
class User():
    '''En esta clase nos dedicamos a crear un diccionario para que cada usuario nuevoi pueda
    ser dado de alta en el sistema'''
    def __init__(self,nombre,password,account):
        self.nombre=nombre
        self.password=password
        self.account=account
    def crear_nuevo_usuario(self):
        '''Agregamos al usuario a nuestro append de cuentas, asi
        como a un diccionario temporal'''
        aux=[]
        usuario={
            self.nombre:{
                'password':self.password,
                'servicios':aux
            }
        }
        self.account.append(usuario)
class Servicio ():
    '''En esta clase se pretende generar los servicios que puede
    tener un usuario, para asi agilizar el proceso'''
    def __init__(self,nombre_usuario,password,nombre_servicio,account):
        self.nombre_usuario=nombre_usuario
        self.password=password
        self.nombre_servicio=nombre_servicio
        self.account=account
        
    def crear_servicio_nuevo(self,index,nuevo_usuario):
        '''En esta funcion se genera y da de alta el nuevo servicio'''
        nuevo_servicio={
            'usuario':nuevo_usuario,
            'password':self.password,
            'NombreServicio':self.nombre_servicio
        }
        self.account[index][self.nombre_usuario]['servicios'].append(nuevo_servicio)
class Documento ():
    def __init__(self,direccion):
        self.direccion=direccion
    def abrir_documento(self):
        file = open(self.direccion, "r")
        nuevo=file.read()
        if (len(nuevo)!=0):
            file = open(self.direccion, "r")
            return True,nuevo
        if (len(nuevo)==0):
            file = open(self.direccion, "r")
            return False,nuevo
    def escribir_json(self,text):
        file2 = open(self.direccion, "w")
        file2.write(str(text))
        file2.close()
