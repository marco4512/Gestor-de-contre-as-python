import json
import ast
from pydoc import doc
from classes import *
from os import system
import getpass
from colorama import Fore, init
'''
Instanciamos el objeto doc que nos servira para acceder
a los metodos de esta clase
'''

doc=Documento('/home/marco/Escritorio/Seguridad en las aplicaciones de software/CRUD/files/jsons.txt')

'''
EL metodo de la clase DOCUMENTO nos retorna
TRUE = El documento tiene contenido 
False = Si el documento esta vacio
ademas nos retorna el str que este dentro de este archivo
'''

abrir_o_no,contenido_archivo=doc.abrir_documento()

'''
Creamos una lista que nos servira como auxiliar para 
el inserte de nuevos usuarios, asi como la modificacion
de servicios etcx
'''

cuentas=[]

'''
Si el archivo no esta vacio procedemos a leer nuestro texto,
pasandolo primero a formato json y llenado con este la lista
con las cuentas que tiene nuestro archivo
'''

if abrir_o_no:
    '''Si el archivo tiene un elemento entonces: '''
    contenido_formato_json = ast.literal_eval(contenido_archivo)
    for key in contenido_formato_json:
        '''Se llena cuentas con los json del archivo'''
        cuentas.append(contenido_formato_json[key])
'''
Creamos un diccionario auxiliar y lo llenamos con
los datos de la lista
'''

mega_dic= {}
for i,cuenta in enumerate(cuentas):
        mega_dic[i]=cuenta
'''
Utilizamos la funcion de json.dups que nos permite
transformar diccionarios en jsons, para de esta forma
poder ingresarlos de nuevo al archivo de txt
'''

json_data = json.dumps(mega_dic,indent=3)

'''
Llamamos a la funcion escribir json que nos permite
añadir el texto a nuestro documento
'''

doc.escribir_json(str(json_data))

'''
Aqui estan algunas funciones utilez para este programa
'''
def ya_existe_el_nombre(nombre_a_buscar):
    '''
    Como su nombre lo indica esta
    funcion se dedica a verificar si
    el usuario existe dentro del archivo
    '''
    list_of_names_aux=[]
    for id,cu in enumerate(cuentas):
        list_of_names_aux.append(list(cu.keys()))
    list_of_names=[]
    for c in list_of_names_aux:
        list_of_names.append(c[0])
    if nombre_a_buscar in list_of_names:
        print(Fore.RED,'Lo síento este nombre ya existe',Fore.WHITE)
        return True
    else:
        return False


def registro(cuentas):
    '''
    En esta funcion nos encargamos de
    registrar de manera exitosa todos
    los nuevos usuarios
    '''
    while True:
        print(f'''
        {'*'*20}REGISTRO{'*'*20}''')
        nombre=input( "Usuario  :   ")
        password=input("Password :   ")
        existe_o_no=ya_existe_el_nombre(nombre)
        if(existe_o_no==False):
            usuario=User(nombre,password,cuentas)
            usuario.crear_nuevo_usuario()
            system('clear')
            break
 
            
def verificar_si_existe(usuario,password,id,mega_dic):
    try:
        if(mega_dic[id][usuario]['password']==password):
            return True
        else:
            return False
    except Exception as e:
        pass
def login_2(aux):
    op=''
    opciones_validas=['1','2']
    if aux==0:
        while True:
            print(''' 
            [1] Iniciar sesion
            [2] Registrarse
            ''')
            op=input('>> ')
            if(op not in opciones_validas):
                system('clear')
                print('Solo Opciones Validas')
            else:
                break
    else:
        op=aux
    if(op=='1'):
        salida=True
        while salida:
            usuario=input( "Nombre Usuario   : ")
            password=getpass.getpass("Ingresa tu contraseña: ")
            existe_o_no=ya_existe_el_nombre(usuario)
            tiene_o_no,contenido_doc = doc.abrir_documento()
            system('clear')
            if (existe_o_no):
                numero=numero_de_cuenta(usuario)
                if (cuentas[numero][usuario]['password']==password):
                    salida=False
                    return True,usuario
                else:
                    print(Fore.RED,'Password Incorrecto, Verifica tus datos',Fore.WHITE)
            else:
                print(Fore.RED,'Usuario Incorrecto, Verifica tus datos',Fore.WHITE)
            if len(contenido_doc)==2:
                system('clear')
                print(Fore.RED,'No tienes cuenta',Fore.WHITE)
                registro(cuentas)
                acualizar_dic(cuentas)
                json_data = json.dumps(mega_dic,indent=3)
                doc.escribir_json(str(json_data))
                salida=False
                return True,usuario
    if(op=='2'):
        registro(cuentas)
        #doc.escribir_en_doc(cuentas)
        json_data = json.dumps(mega_dic,indent=3)
        #doc.escribir_json(str(json_data))
        print('Registro exitoso, recarge el programa')
        for i,cuenta in enumerate(cuentas):
            mega_dic[i]=cuenta
        #doc.escribir_en_doc(cuentas)
        json_data = json.dumps(mega_dic,indent=3)
        doc.escribir_json(str(json_data))
        return 'Registrado',''

def login(usuario,password,cuentas,mega_dic):
    cont=0
    for id in mega_dic:
        if(cont!=len(cuentas)):
            if(verificar_si_existe(usuario,password,id,mega_dic)):                
                return True
                break
            else:
                cont+=1
        else:
            print('no se encontro cuenta, registrate para continuar')
            cont=0
            return False
            break
def numero_de_cuenta(nombre_usuario):
    for numero in mega_dic:
        for x in mega_dic[numero]:
            if(x==nombre_usuario):
                return(numero)
def acualizar_dic(cuentas):
    for i,cuenta in enumerate(cuentas):
        mega_dic[i]=cuenta

def editar_registros(mega_dic,cuentas,usuario,indice):

    acualizar_dic(cuentas)
    usuario=''
    for nombre in cuentas[indice]:
        usuario=nombre
    print(f'''
    {'*'*20}MENU DE EDICION{'*'*20}
    {Fore.GREEN}[1]Nombre usuario
    {Fore.RED}[2]Password
    {Fore.CYAN}[3]Servicio''')
    opcion=input('>> ')

    if (opcion=='1'):
        print(F'''
        {Fore.GREEN}{'*'*20} REGISTROS {'*'*20}''')
        old_name=''
        for x in cuentas[indice]:
            old_name=x
            print(f''' 
            Nombre actual | {Fore.RED}{str(x)}{Fore.GREEN}
            INGRESA EL NUEVO NOMBRE''')
        nuevo_nombre=input('>> ')
        list_of_names_aux=[]
        for id,cu in enumerate(cuentas):
            list_of_names_aux.append(list(cu.keys()))
        list_of_names=[]
        for c in list_of_names_aux:
            list_of_names.append(c[0])
        if (nuevo_nombre in list_of_names):
            print(Fore.RED,'Este nombre ya esta ocupado')
        else:
            registro_editado={
                nuevo_nombre:cuentas[indice][old_name]
            }
            cuentas[indice]=registro_editado
            acualizar_dic(cuentas)
            #doc.escribir_en_doc(str(cuentas))2
            json_data = json.dumps(mega_dic,indent=3)
            doc.escribir_json(str(json_data))
            
    if (opcion=='2'):
        nueva=input(f'{Fore.RED}Ingresa la nueva contraseña: ')
        print(type(indice),indice,type(usuario),usuario,type(nueva))
        
        cuentas[indice][usuario]['password']=nueva
        #doc.escribir_en_doc(str(cuentas))
        json_data = json.dumps(mega_dic,indent=3)
        doc.escribir_json(str(json_data))

    if(opcion=='3'):
        list_of_options=['1','2','3','4']
        print(f'''
        {'*'*20} SERVICIOS {'*'*20}''')
        if(len(cuentas[indice][usuario]['servicios'])!=0):
            while True:
                try:
                    for i,x in enumerate(cuentas[indice][usuario]['servicios']):
                        print(f'[{i}] {x}')
                    print(f'''{Fore.GREEN}
                    Selecciona el servicio a editar''' )
                    op=input('>>')
                    system('clear')
                    print(f'''Servicio seleccionado
                    {Fore.RED}{cuentas[indice][usuario]['servicios'][int(op)]}''')
                    break
                except:
                    print(Fore.RED,'Seleccion invalida',Fore.GREEN)
            while True:
                print(f'''{Fore.GREEN}
                {'*'*20}¿ Que deseas editar ? {'*'*20}
                [1]Usuario
                [2]Password
                [3]Nombre_Serv
                [4]Todo''')
                el=input('>> ')
                system('clear')
                if el in list_of_options:
                    break
            usuario_old=cuentas[indice][usuario]['servicios'][int(op)]['usuario']
            password_old=cuentas[indice][usuario]['servicios'][int(op)]['password']
            NombreServicio_old=cuentas[indice][usuario]['servicios'][int(op)]['NombreServicio']
            if (el=='1' or el=='4'):
                usuario_old=input('Ingresa el nuevo usuario :')
            if(el=='2'or el=='4'):
                password_old=input('Ingresa la nueva contraseña: ')
            if(el=='3' or el=='4'):
                NombreServicio_old=input('Ingresa el nombre del servicio: ')
            nuev={
                'usuario': usuario_old, 
                'password': password_old, 
                'NombreServicio': NombreServicio_old
            }
            cuentas[indice][usuario]['servicios'][int(op)]=nuev
            acualizar_dic(cuentas)
            #doc.escribir_en_doc(str(cuentas))
            print(cuentas[indice][usuario]['servicios'][int(op)])
            json_data = json.dumps(mega_dic,indent=3)
            doc.escribir_json(str(json_data))
        else:
            system('clear')
            print(Fore.RED,'No tienes servicios',Fore.GREEN)

def opciones_del_menu(nombre_usuario,op,mega_dic,cuentas,indice_aux):
    system('clear')
    indice=indice_aux
    if(op=='1'):
        print('*'*20,f'Nuevo Servicio para {nombre_usuario}','*'*20)
        nombre_servicio=input(f"Nombre del {Fore.RED}SERVICIO: {Fore.GREEN} ")
        password=input(f"Ingresa su {Fore.RED}PASSWORD: {Fore.GREEN}")
        nuevo_usuario=input(f"Ingresa el {Fore.RED}USUARIO: {Fore.GREEN}")
        servicio=Servicio(nombre_usuario,password,nombre_servicio,cuentas)
        servicio.crear_servicio_nuevo(indice,nuevo_usuario)
        #doc.escribir_en_doc(cuentas)
        json_data = json.dumps(mega_dic,indent=3)
        doc.escribir_json(str(json_data))
        print('*'*20,'Alta Exitosa','*'*20)
        system('clear')
        return True
    if(op=='2'):
        print('*'*20,'Elige tu servicio a borrar','*'*20)
        for i,servicios in enumerate(cuentas[indice][nombre_usuario]['servicios']):
            print(f"[{i}]|USUARIO:\t{servicios['usuario']}\t|SERVICIO:\t{servicios['NombreServicio']}\t|PASSWORD:\t{servicios['password']}\t|")
        indice_a_borrar=int(input(">> "))
        aux=cuentas[indice][nombre_usuario]['servicios'][indice_a_borrar]
        print('*'*20,'¿Seguro deseas borrar?','*'*20)
        print(f"[{indice_a_borrar}]|USUARIO:\t{aux['usuario']}\t|SERVICIO:\t{aux['NombreServicio']}\t|PASSWORD:\t{aux['password']}\t|")
        borrar=int(input("[1] SI [2]| NO >> "))
        if borrar==1:
            print('*'*20,'Se elimino correctamente','*'*20)
            cuentas[indice][nombre_usuario]['servicios'].pop(indice_a_borrar)
            #doc.escribir_en_doc(cuentas)
            json_data = json.dumps(mega_dic,indent=3)
            doc.escribir_json(str(json_data))
        else:
            print('*'*20,'Borrado cancelado','*'*20)
        system('clear')
        return True
    if(op=='3'):
        editar_registros(mega_dic,cuentas,nombre_usuario,indice)
      
        return True
def menu_usuario(usuario):
    index=numero_de_cuenta(usuario)
    cont=True
    opciones_validas=['1','2','3','4']
   
    while cont:
        nombre_us=''
        for x in cuentas[index]:
            nombre_us=x
        print(Fore.GREEN,f'''
        HOLA {Fore.LIGHTRED_EX}{nombre_us.upper()}{Fore.GREEN} ELIGE UNA OPCION
        {'*'*20}MENU{'*'*20}
        [1] INSERTAR SERVICIO
        [2] ELIMINAR  SERVICO
        [3] EDICION  DE DATOS
        [4] Salir
        ''')
        opcion=input(">> ")
        if (opcion not in opciones_validas):
            system('clear')
            print(Fore.RED,'Opcion no valida',Fore.GREEN)
            cont=True
        else:
            cont=opciones_del_menu(usuario,opcion,mega_dic,cuentas,index)
            for i,cuenta in enumerate(cuentas):
                mega_dic[i]=cuenta
        if(opcion=='4'):
            print(Fore.RED,'Gracias',Fore.GREEN)
            cons=False
            break
system('clear')     
estado,user_name=login_2(0)
continuar=True
if estado =='Registrado':
    estado2,user_name=login_2('1')
    if(estado2):
        system('clear')
        menu_usuario(user_name)
elif(estado):
    system('clear')
    menu_usuario(user_name)
