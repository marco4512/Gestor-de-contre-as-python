import json
import hashlib
import ast
from pydoc import doc
from classes import *
from os import system
import getpass
from colorama import Fore, init
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from tqdm import *
key=''
'''
Instanciamos el objeto doc que nos servira para acceder
a los metodos de esta clase
'''
lista_de_servicios=[]
def generar_key(password_encrip):
    password = bytes(password_encrip,encoding = "utf-8")
    salt = password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    #print('llave encriptado',key,type(key))
    return(key)
def cargar_servicios(user_name,password):
    print(Fore.GREEN,'Cargado Datos')
    id=numero_de_cuenta(user_name)
    lista=[]
    for x in tqdm(cuentas[id][user_name]['servicios']):
        ser=des(password,x['NombreServicio'])
        ser=de_bin_a_string(ser)
        pas=des(password,x['password'])
        pas=de_bin_a_string(pas)
        usr=des(password,x['usuario'])
        usr=de_bin_a_string(usr)
        if ([usr,pas,ser] not in lista_de_servicios):
            lista_de_servicios.append([usr,pas,ser])
def re_ecrip_contreña(new_password):
    new_service_encripted=[]
    new_password=has(new_password)
    print('Actualizando datos..')
    for x in lista_de_servicios:
        dic_temp={
            'usuario':str(encript(new_password,x[0])),
            'password':str(encript(new_password,x[1])),
            'NombreServicio':str(encript(new_password,x[2]))
        }
        new_service_encripted.append(dic_temp)
    
    return(new_service_encripted)

    pass


def de_bin_a_string(bin):
    bin=str(bin).replace("b'","")
    bin=bin[:len(bin)-1]
    return bin

def encript(password_cript,value):
    key=generar_key(password_cript)
    f = Fernet(key)
    values=bytes(value,encoding = "utf-8")
    token = f.encrypt(values)
    return token
def des(password_cript,valor):
    valor= valor.replace("b'",'')
    valor=valor[:len(valor)-1]
    valor=bytes(valor,encoding='utf-8')
    #print(type(valor),'___',valor)
    key=generar_key(password_cript)
    #print('recibiendo llave :',key)
    f = Fernet(key)
    token = f.decrypt(valor)
    return token




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

        '''
        Metemos un ciclo while para que
        si ocurre algun error al momento
        de hacer le registro
        este nos pida los datos de nuevo
        '''

        print(f'''
        {'*'*20}REGISTRO{'*'*20}''')
        nombre=input( "Usuario  :   ")
        password=input("Password :   ")

        '''
        En caso de que el usuario ya exista
        nos dara una alerta y repetira el proceso
        en caso de que no rompera el ciclo
        y registrara al usuario
        '''

        existe_o_no=ya_existe_el_nombre(nombre)
        if(existe_o_no==False):
            password=str(has(password))
            key=str(has2(password))
            #usuario=str(has2(usuario))
            usuario=User(nombre,password,cuentas)
            usuario.crear_nuevo_usuario()
            system('clear')
            break
 
def login_2(aux):

    '''
    Esta es una de las funciones mas largas
    esta funcion nos permite de manera directa
    saber que es lo que el usuario desea hacer
    si ingresar con su cuenta o crear una nueva
    asi mismo nos permite redirigir a otras funciones
    '''
    
    op=''

    '''
    Declaramos un par de variables que necesitamos
    que el usuario se apege a ellas y no introduzca datos
    erroneos
    '''

    opciones_validas=['1','2']

    '''
    Al hacer esta comparacion, lo que hacemos en realida es
    decirle al codigo que el usuario no ha intentado ingresar
    a otra opcion, o sea es la primera vez que este ingresara 
    al menu de inicio de secion
    '''

    if aux==0:

        '''
        Al igual que otras validaciones, esta
        nos sirve para obligar al usuario a 
        ingresar solo valores del menu
        repitiendolo hasta que ingrese lo correcto
        '''

        while True:
            print(''' 
            [1] Iniciar sesion
            [2] Registrarse
            ''')
            op=input('>> ')

            '''
            Se valida que lo que ingresa este
            en las opciones validas
            '''

            if(op not in opciones_validas):
                
                '''
                EN CASO DE NO ACATAR
                SE LANZA EL MENSAJE Y SE LIMPIA
                LA PANTALLA
                '''

                system('clear')
                print('Solo Opciones Validas')
            else:

                '''
                Rompemos el ciclo cuando la opcion es
                valida
                '''

                break
    else:

        '''
        En caso de que no sea la primera vez que se
        corre el menu, se asigna a la opcion del menu
        el valor de axiliar mandado desde otra funcion
        en este caso se pretende que llege diercto a la opcion
        1 que es login
        '''

        op=aux

    if(op=='1'):

        '''
        En la opcion de login se valida que el usuaario
        y la contreña sean correctos
        para ello tambien utilizamos un while
        '''

        salida=True

        '''
        Salia nos permite saber cuando queremos
        terminar el ciclo 
        '''

        while salida:
            
            '''
            Este ciclo se repite hasta que el usuario
            y la contraseña sean correctos
            '''

            usuario=input( "Nombre Usuario   : ")

            '''
            getpass nos permite ocultrar el input del
            usuario, esto es usual en el ingreso de
            contraseñas en consola
            '''

            password=getpass.getpass("Ingresa tu contraseña: ")
            password=has(password)
            
            '''
            Verificamos que el usario exista en nuestro txt,
            para si poder continuar o no con el proceso
            '''

            existe_o_no=ya_existe_el_nombre(usuario)
            
            '''
            Verificamos el contenido de nuestro txt,
            en ocaciones se nos genera solo un
            {} el cual no permite agregar usuarios
            sin embargo con otro metodo lo resolveremos
            '''

            tiene_o_no,contenido_doc = doc.abrir_documento()
            
            '''
            Limpiamos la pantalla
            '''
            
            system('clear')

            '''
            hacemos una condicional con el estado de la variable "existe_o_no"
            cuyo valor puede ser True o False
            '''

            if (existe_o_no):

                '''
                En caso de True , entonces se verifica que la contraseña sea igual
                a la que el usuario ingreso
                '''

                numero=numero_de_cuenta(usuario)
                if (cuentas[numero][usuario]['password']==password):
                    
                    '''
                    En caso de ser cierto se cierra el ciclo
                    y se retorna un TRue mas el usuario para futuras funciones'''
                    cargar_servicios(usuario,password)
                    print(lista_de_servicios)
                    salida=False
                    return True,usuario

                else:

                    '''
                    En caso de ser falso se notifica el error
                    de contraseña
                    '''

                    print(Fore.RED,'Password Incorrecto, Verifica tus datos',Fore.WHITE)
            else:

                '''
                Si no se encuentra el usuario, se notifica
                que este esta incorrecto
                '''

                print(Fore.RED,'Usuario Incorrecto, Verifica tus datos',Fore.WHITE)
            if len(contenido_doc)==2:

                '''
                En este caso especial, cuando no se tiene 
                registro alguno, o que tenemos nuestro
                json vacio lo que se realiza es notificar
                al usuario que es obligatorio registrarse
                '''

                system('clear')
                print(Fore.RED,'No tienes cuenta',Fore.WHITE)

                '''
                Se llama a la funcion de registro
                '''

                registro(cuentas)

                '''
                Actualizamos nuestro diccionario axiliar
                '''

                acualizar_dic(cuentas)

                '''
                Trasnformamos este a un json 
                para posteriormente utilizar
                el metodo escribir_json de la
                clase documento con nuestro json ya
                indentado
                '''

                json_data = json.dumps(mega_dic,indent=3)
                doc.escribir_json(str(json_data))

                '''
                Cerramos el ciclo y retornamos
                true asi como el nombre del usuario
                '''
                
                salida=False
                return True,usuario
    if(op=='2'):
        
        '''
        En caso de que el usuario
        eliga la opcion de registrarse
        entonces mandamos llamar a la funcion
        registro
        '''

        registro(cuentas)

        '''
        Se carga el json con los valores nuevos agregados
        asi como la acutualizacion de nuestro diccionario
        auxiliar, Notificando del exito de este registro
        '''

        acualizar_dic(cuentas)
        json_data = json.dumps(mega_dic,indent=3)
        print('Registro exitoso')

        '''
        Escribimos en el txt nuestro nuevo elemento
        json 
        '''

        doc.escribir_json(str(json_data))
        return 'Registrado',''

def numero_de_cuenta(nombre_usuario):
    
    '''
    Esta fucion prente obtener el numero
    de ID de cada uno de los usuarios
    que existan en el sistema
    '''

    for numero in mega_dic:

        '''
        Recorremos nuestro diccionario
        auxiliar para optener las llaves 
        de cada item del diccionario
        '''

        for x in mega_dic[numero]:

            '''
            Recorrremos cada item con su llave
            para obtener el nombre del usuario
            y de esta forma comparar con nuestro valor
            de usuario a buscar
            '''

            if(x==nombre_usuario):

                '''
                Si el valor que se muestra 
                es igual al que se busca se 
                retorna
                '''
                
                return(numero)

def acualizar_dic(cuentas):

    '''
    Esta funcion permite, actulizar
    nuestro diccionario auxiliar
    con un arreglo temporal
    '''

    for i,cuenta in enumerate(cuentas):
        
        '''
        Se llena con
        los valores del arrelgo
        temporal asignando un id
        '''

        mega_dic[i]=cuenta

def editar_registros(mega_dic,cuentas,usuario,indice):
    
    '''
    En esta funcion se pretende abordar
    todos los tipos de ediciones que se pueden+
    realizar en el archivo. Para ello primero
    actuañizamos el diccionario
    '''
    
    acualizar_dic(cuentas)

    '''
    Una vez actualizado obtenemos el nombre del usuario
    por medio de el indice, esto se hace de esta forma
    porque en caso de que exista algun cambio de nombre
    durante la ejecucion del programa, esto nos permite
    siempre obtener directamente del archivo txt, el ultimo
    nombre guardado en el evitando errores de no actualizacion
    '''
    
    usuario=''
    
    for nombre in cuentas[indice]:
        usuario=nombre

    '''
    Una vez que se obtiene el nombre
    se muestra  una lista con  las
    opciones de edicion que se tienen
    '''

    print(f'''
    {'*'*20}MENU DE EDICION{'*'*20}
    {Fore.GREEN}[1]Nombre usuario
    {Fore.RED}[2]Password
    {Fore.CYAN}[3]Servicio''')
    opcion=input('>> ')

    if (opcion=='1'):

        '''
        Si se eligio cambiar el nombre de usuario
        lo primero que se mostrara sera un aviso
        con el nombre anterior de este mismo
        antes de cambiarlo
        '''

        print(F'''
        {Fore.GREEN}{'*'*20} REGISTROS {'*'*20}''')
        
        '''
        Se guarda el nobre viejo para posteriores
        usos
        '''

        old_name=usuario
        print(f''' 
        Nombre actual | {Fore.RED}{usuario}{Fore.GREEN}
        INGRESA EL NUEVO NOMBRE''')
        nuevo_nombre=input('>> ')

        '''
        Se  verifica que exista este nombre
        para en caso de que si,lo haga notifique
        al usuario de ello
        '''

        existe_o_no=ya_existe_el_nombre(nuevo_nombre)

        if(not existe_o_no):

            '''
            Si no existe entonces
            se procede a hacer el cambio de
            nombre.Para ello se genera un diccionario
            clon, con todos los datos de este usuario
            sin el nombre de el, si no con el nuevo
            '''

            registro_editado={
                nuevo_nombre:cuentas[indice][old_name]
                }

            '''
            reasignamos a nuestro arreglo temporal
            el valor de nuestro nuevo diccionario,dado
            en el mismo ID un cambio de usuario, pero conservando
            todos los datos de este
            '''

            cuentas[indice]=registro_editado
            
            '''
            Actualizamos el diccionario con nuestros
            datos nuevos
            '''
            
            acualizar_dic(cuentas)
            
            '''
            Creamos de nuevo el json y lo escribimos en nuestro txt
            '''
            
            json_data = json.dumps(mega_dic,indent=3)
            doc.escribir_json(str(json_data))
            
    if (opcion=='2'):

        '''
        Si se elige la opcion de cambiar contraseña
        como primera instancia se necesita que el usuario ingrese la nueva
        contreña
        '''
        nueva=input(f'{Fore.RED}Ingresa la nueva contraseña: ')
        lista_nueva=re_ecrip_contreña(nueva)
        nueva=has(nueva)
        '''
        Se remplaza la contraseña vieja con la contraseña nueva
        en el arreglo temporal
        '''
        cuentas[indice][usuario]['password']=nueva
        cuentas[indice][usuario]['servicios']=lista_nueva
        acualizar_dic(cuentas)
        '''
        Se genera el json y guarda en el txt
        '''
        
        json_data = json.dumps(mega_dic,indent=3)
        doc.escribir_json(str(json_data))

    if(opcion=='3'):

        '''
        Si se elige la opcion de editar servicios
        para ello primero se genera una lista con
        los valores que son permitidos 
        '''

        list_of_options=['1','2','3','4']
        
        '''
        En esta parte mostramos en pantalla
        todos los servicios que esto usuario
        tiene registrados
        '''
        
        print(f'''
        {'*'*20} SERVICIOS {'*'*20}''')
        
        '''
        Se hace una condicion que nos permite
        saber si el usuario tiene o no servicios
        registrados
        '''

        if(len(cuentas[indice][usuario]['servicios'])!=0):
            
            '''
            En caso de que este usuario tenga al menos un servicio
            se mostraran estos
            '''
            
            while True:

                '''
                Se entra en un ciclo que nos mostrara
                los servicios y las opciones de estos hasta
                que se eliga una opcion  valida
                '''

                try:

                    '''
                    Impresion de los servicios
                    '''

                    for i,x in enumerate(lista_de_servicios):
                        print(f'[{i}] Usuario:\t{x[0]}| Password:\t{x[1]}| Servicio: {x[2]}|')
                    
                    print(f'''{Fore.GREEN}
                    Selecciona el servicio a editar''' )
                    op=input('>>')
                    
                    '''
                    Se limpia la pantalla
                    y se recibe la opcion del servicio que se quiere editar
                    '''
                    
                    system('clear')
                    
                    '''
                    Se imprime el servicio seleccionado
                    '''
                    seleccioando=f'[{int(op)}] Usuario:\t{lista_de_servicios[int(op)][0]}| Password:\t{lista_de_servicios[int(op)][1]}| Servicio: {lista_de_servicios[int(op)][2]}|'
                    print(f'''Servicio seleccionado
                    {Fore.RED}{seleccioando}
                    ''')
                    
                    '''
                    Se rompe el ciclo
                    '''
                    break
                except:
                    
                    '''
                    En caso de que se seleccione
                    una opcion que no sea un registro
                    este catch nos ayudara a mostar este
                    aviso
                    '''
                    
                    print(Fore.RED,'Seleccion invalida',Fore.GREEN)
            while True:

                '''
                Se entra en otro ciclo que pretende
                validar que el usuario ingrese una
                opcion corecta
                '''

                print(f'''{Fore.GREEN}
                {'*'*20}¿ Que deseas editar ? {'*'*20}
                [1]Usuario
                [2]Password
                [3]Nombre_Serv
                [4]Todo''')

                el=input('>> ')
                system('clear')
                if el in list_of_options:
                    
                    '''
                    Si lo que se elige esta
                    dentro de las opciones que se 
                    tienen entonces se rompe el ciclo
                    '''

                    break
            
            '''
            se declaran variable con los nombres
            de todos los valores que tiene el servicio
            seleccionado, para de esta forma sustituirlo
            con la opcion que se eliga, si se elige la opcion
            4 entrara en todos los if, sustituyendo los valores
            viejos con los ingresados por el usuario
            '''
            usuario_old=cuentas[indice][usuario]['servicios'][int(op)]['usuario']
            password_old=cuentas[indice][usuario]['servicios'][int(op)]['password']
            NombreServicio_old=cuentas[indice][usuario]['servicios'][int(op)]['NombreServicio']

            if (el=='1' or el=='4'):
                usuario_old=input('Ingresa el nuevo usuario :')
                usuario_old=str(encript(cuentas[indice][usuario]['password'],usuario_old))
            if(el=='2'or el=='4'):
                password_old=input('Ingresa la nueva contraseña: ')
                password_old=str(encript(cuentas[indice][usuario]['password'],password_old))
            if(el=='3' or el=='4'):
                NombreServicio_old=input('Ingresa el nombre del servicio: ')
                NombreServicio_old=str(encript(cuentas[indice][usuario]['password'],NombreServicio_old))
            '''
            Se genera el nuevo diccionario
            con todos los elementos
            que se modificaron
            '''
            
            nuev={
                'usuario': usuario_old, 
                'password': password_old, 
                'NombreServicio': NombreServicio_old
            }
            
            '''
            Se anexa al arreglo temporal para hacer el cambio
            '''
            cuentas[indice][usuario]['servicios'][int(op)]=nuev
            acualizar_dic(cuentas)
            
            '''
            se actualiza y se muestra el servicio modificado
            y a su vez se rescribe el documento
            '''
            lista_de_servicios.pop(indice)
            cargar_servicios(usuario,cuentas[indice][usuario]['password'])
            print(f'[{int(op)}] Usuario:\t{lista_de_servicios[int(op)][0]}| Password:\t{lista_de_servicios[int(op)][1]}| Servicio: {lista_de_servicios[int(op)][2]}|')
            json_data = json.dumps(mega_dic,indent=3)
            doc.escribir_json(str(json_data))
        else:
            
            '''
            si esta vacio el arreglo
            entonces se notifica al usuario
            '''

            system('clear')
            print(Fore.RED,'No tienes servicios',Fore.GREEN)

def opciones_del_menu(nombre_usuario,op,mega_dic,cuentas,indice_aux):
    
    '''
    Se obtiene el nombre del json
    '''
    
    nombre_usuario=''
    for nombre in cuentas[indice_aux]:
        nombre_usuario=nombre
    
    
    '''
    En esta funcion se pretende canalizar las 
    opciones que el menu principal para realizar 
    las otras funciones
    '''

    system('clear')
    if(op=='1'):
        
        '''
        Si se elige la opcion de agregar un nuevo servicio
        entonces se solicitaran los datos de este
        '''
        
        print('*'*20,f'Nuevo Servicio para {nombre_usuario}','*'*20)
        nombre_servicio=input(f"Nombre del {Fore.RED}SERVICIO: {Fore.GREEN} ")
        password=input(f"Ingresa su {Fore.RED}PASSWORD: {Fore.GREEN}")
        nuevo_usuario=input(f"Ingresa el {Fore.RED}USUARIO: {Fore.GREEN}")
        nombre_servicio=str(encript(cuentas[indice_aux][nombre_usuario]['password'],str(nombre_servicio)))
        password=str(encript(cuentas[indice_aux][nombre_usuario]['password'],str(password)))
        nuevo_usuario=str(encript(cuentas[indice_aux][nombre_usuario]['password'],str(nuevo_usuario)))
        '''
        password=str(has2(password))
        nuevo_usuario=str(has2(nuevo_usuario))'''
        
        '''
        se genera el objeto servicio el cual
        nos servira para generar un diccionario
        con esos datos en particular
        '''
        servicio=Servicio(nombre_usuario,password,nombre_servicio,cuentas)
        servicio.crear_servicio_nuevo(indice_aux,nuevo_usuario)
        cargar_servicios(nombre_usuario,cuentas[indice_aux][nombre_usuario]['password'])
        '''
        Se crea el json y se escribe en el txt
        '''

        json_data = json.dumps(mega_dic,indent=3)
        doc.escribir_json(str(json_data))
        print('*'*20,'Alta Exitosa','*'*20)
        system('clear')
        
        '''
        Se notifica del alta exitosa y se retorna un True
        '''

        return True
    if(op=='2'):
        
        '''
        Si se elige la opcion de borrar
        entonces se solicita la seleccion de
        alguno de los servicios que existen
        '''
       
        if(len(cuentas[indice_aux][nombre_usuario]['servicios'])!=0):

            print('*'*20,'Elige tu servicio a borrar','*'*20)
            
            '''
            Se imprime los servicios que tiene el usuario
            '''
            for i,servicios in enumerate(lista_de_servicios):
                '''print('servicio encriptado',servicios['NombreServicio'])
                print('Contraseña usuario',cuentas[indice_aux][nombre_usuario]['password'])
                '''
                print(f"[{i}]|USUARIO:\t{servicios[0]}\t|SERVICIO:\t{servicios[2]}\t|PASSWORD:\t{servicios[1]}\t|")
           
            '''
            Se entra en un ciclo que obliga al usuario
            a ingresar una opcion de servicio correcta
            '''
            while True:
                try:

                    '''
                    Se pide la opcion y si esta se ecunetra
                    dentro de los servicios que se tienen 
                    entonces se pide una confirmacion para
                    eliminarlo
                    '''
                    indice_a_borrar=int(input(">> "))
                    aux=lista_de_servicios[indice_a_borrar]
                    print('*'*20,'¿Seguro deseas borrar?','*'*20)
                    print(aux)
                    break
                except :
                    
                    '''
                    En caso de que no se encuentre ningun servicio se 
                    notifica al usuario
                    '''
                    
                    print('No se econtro servicio')
            
            '''
            Se confirma si se quiere eliminar o no
            '''

            borrar=int(input("[1] SI [2]| NO >> "))
            if borrar==1:
                
                '''
                Si se elige esta opcion se hace el borrado
                y se actualiza en el txt
                '''

                print('*'*20,'Se elimino correctamente','*'*20)
                cuentas[indice_aux][nombre_usuario]['servicios'].pop(indice_a_borrar)
                json_data = json.dumps(mega_dic,indent=3)
                doc.escribir_json(str(json_data))
                lista_de_servicios.pop(indice_a_borrar)
                
            else:
                print('*'*20,'Borrado cancelado','*'*20)
            system('clear')
            return True
        else:
            print('Sin Servicios')
            return True

    if(op=='3'):
        '''
        SI se desea editar un registro se manda a 
        llamar esta opcion
        '''
        editar_registros(mega_dic,cuentas,nombre_usuario,indice_aux)
        return True

def menu_usuario(usuario):
    
    '''
    En esta funcion se muestra
    y recibe el menu principal
    Se asigna el valor del ID
    asi como los valores que
    son validos para el ingreso
    de ellos
    '''

    index=numero_de_cuenta(usuario)
    cont=True
    opciones_validas=['1','2','3','4']

    '''
    Se entra a un ciclo que permite
    pedir solo opciones validas al usuario
    '''
   
    while cont:
        
        '''
        Obtenemos del ultimo valor
        del nombre directo del json
        '''

        nombre_us=''
        for x in cuentas[index]:
            nombre_us=x
        
        '''
        Informamos al usuario cuales son las opciones
        del programa
        '''

        print(Fore.GREEN,f'''
        HOLA {Fore.LIGHTRED_EX}{nombre_us.upper()}{Fore.GREEN} ELIGE UNA OPCION
        {'*'*20}MENU{'*'*20}
        [1] INSERTAR SERVICIO
        [2] ELIMINAR  SERVICO
        [3] EDICION  DE DATOS
        [4] Salir
        ''')
        opcion=input(">> ")
        
        '''
        Si la respuesta del usuario no esta dentro de las deseadas
        entonces se repite el ciclo y se le informa a este de ello
        '''

        if (opcion not in opciones_validas):
            system('clear')
            print(Fore.RED,'Opcion no valida',Fore.GREEN)
            cont=True
        else:

            '''
            En caso de que si sea valida la opcion se
            actualiza y manda a llamar a la funcion opciones
            del menu
            '''

            cont=opciones_del_menu(usuario,opcion,mega_dic,cuentas,index)
            acualizar_dic(cuentas)
        if(opcion=='4'):
           
            '''
            En caso de que se deese salir del programa
            se rompe el ciclo
            '''

            print(Fore.RED,'Gracias',Fore.GREEN)
            cons=False
            break
def has(m):
    mensaje=m  
    m=hashlib.sha256(mensaje.encode())
    return(m.hexdigest())
def has2(m):
    mensaje=m  
    m=hashlib.sha512(mensaje.encode())
    return(m.hexdigest())

'''
Al inciar el programa se 
limpia la consola dejando
solo las opciones de 
inicio de sesion y
la de registro
'''     

system('clear')     

'''
Se manda a llamar a la funcion
login la cual llevara como
parametro la opcion 0 que representa
a un primer recorrido de esta
recibiendo como regreso un estado y
el nombre del usuario
'''
try:
    estado,user_name=login_2(0)

    '''
    se pregunta si la respuesta
    de regreso de la primera 
    interaccion con el login
    es true o registrado
    '''

    if estado =='Registrado':

        '''
        En caso de que si sea registrado,
        nos indica que ya se registro este
        en el primer login por lo que llamaremos 
        de nuevo a login para asi entrar directo
        al login sin salir del programa
        '''

        estado2,user_name=login_2('1')
        
        '''
        se vuelve a hacer una condicion que 
        si es verdadera entra directo a la funcion de
        menu
        '''
        if(estado2):
            system('clear')
            '''
            Se llama a la funcion menu
            '''

            menu_usuario(user_name)
    elif(estado):
        system('clear')
        '''
        Si se logio correctamente
        se va directo al menu
        '''
        menu_usuario(user_name)
except Exception as e:
    print(e)
    print('Sucedio un error, reinicia el programa')

