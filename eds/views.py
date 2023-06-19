from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from eds.models import Surtidores, Companias, Registroseriales, Cierreseriales, Facturas, RegistroTanques, MedidasTanques, Tanques, Aplicaciones,  CierreVentasDia
from .forms import RegistroserialesForm, FacturasForm, RegistroTanquesForm, VolumenTanquesForm, BusVolumenTanquesForm
from django.contrib import messages
from datetime import datetime, timedelta, time, date



def eds (request):
    return render(request, 'eds.html')

def home (request):
    return render(request, 'home.html')


def panel (request):
    listas = Aplicaciones.objects.all()
    return render(request, 'panel.html', { 'listas':listas })

def autenticar (request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': UserCreationForm})
    else: 
        if request.POST['password1'] == request.POST['password2']:
            #registra usuario
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('panel') 
            except IntegrityError:              
                 return render(request, 'login.html', {
                    'form': UserCreationForm,
                    'error': 'Usuario ya Existe'    
                })     
            
        return render(request, 'login.html', {
                'form': UserCreationForm,
                'error': 'Contrasena no coincide'    
        })
    
    
def cerrarsesion(request):
    logout(request)
    return redirect('/')  
        
def iniciar(request):
    if request.method == 'GET':
        return render(request, 'iniciar.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, 
                     username=request.POST['username'], 
                     password=request.POST['password'] )
        if user is None:
            messages.warning(request, 'Usuario o Password Incorreccto')

            return render(request, 'iniciar.html', {
                'form': AuthenticationForm                
            })
        else: 
            login(request, user)
            
            return redirect('panel')
        
def registroserialdiario(request):
    #messages.success(request, 'Your password was updated successfully!')  
    cia = Companias.objects.get(usuario=request.user)   
    surtidores = Surtidores.objects.filter(cia = cia.pk)  
    #seriales = Registroseriales.objects.filter(cia = cia.pk )    
    seriales = Registroseriales.objects.filter(cia = cia.pk, estatus=False ).order_by('-id')
   
    if request.method == 'GET':
        return render(request, 'registroserialdiario.html', {
            'form' : RegistroserialesForm,
            'seriales': seriales,
            'surtidores': surtidores

        } )      
    else:
        try:
            mensaje = "No se pudo guardar"
            identificador_surtidor = request.POST['identificador']
            ultimoserial = Registroseriales.objects.filter(cia = cia.pk, identificador= identificador_surtidor ).last()
            compania = Companias.objects.get(usuario=request.user)        
            formulario = RegistroserialesForm(request.POST)
            nuevo = formulario.save(commit=False)
            nuevo.usuario = request.user   
            nuevo.cia = Companias.objects.get(usuario=request.user)
            nuevo.serialinicio = ultimoserial.serialfinal 
            serfinal = request.POST['serialfinal']
            
            #if not(ultimoserial):
            #    mensaje = "error"
                           
            #verificar si el serial final es mayor
            if int(serfinal) > int(ultimoserial.serialfinal):   
                cambiar_estado = Surtidores.objects.filter(cia = cia.pk, id = identificador_surtidor).update(cierre=True)        
                litros = int(serfinal) - ultimoserial.serialfinal
                nuevo.totallitros = litros
                nuevo.save()
                
                messages.success(request, 'Serial Registrado')

                return redirect('registroserialdiario')
                
                #return render(request, 'registroserialdiario.html', {
                #'form' : RegistroserialesForm,
                #'error': litros
                #} )  
            
            else:
                messages.warning(request, 'El serial debe ser mayor al inicial')
                
                return render(request, 'registroserialdiario.html', {
                'form' : RegistroserialesForm,
                'seriales': seriales,
                'surtidores': surtidores
                
                } )  
            
            
        except ValueError:        
            return render(request, 'registroserialdiario.html', {
            'form' : RegistroserialesForm,
            'seriales': seriales,
            'surtidores': surtidores

        } )     
            
       
        
def listaseriales(request):
    cia = Companias.objects.get(usuario=request.user) 
    surtidores = Surtidores.objects.filter(cia = cia.pk)           
    seriales = Registroseriales.objects.filter(cia = cia.pk ).order_by('-id')
    #seriales = Registroseriales.objects.filter(cia = cia.pk, estatus=False )
    return render(request, 'listaseriales.html', 
        { 'seriales': seriales, 
        'surtidores': surtidores
        }              
    )             
    

def cierreserial(request):
    cia = Companias.objects.get(usuario=request.user)   
    surtidores = Surtidores.objects.filter(cia = cia.pk)  
    seriales = Registroseriales.objects.filter(cia = cia.pk, estatus=False)   

    
    if request.method == 'GET':
        return render(request, 'cierreserial.html', {
            'seriales': seriales,
            'surtidores': surtidores

        } )      
    else:
        try:
            mensaje = "No se pudo guardar"
            current_date = date.today()  
            
            id_surtidor = request.POST['id_serial']
            serial_inicial = Registroseriales.objects.filter(cia = cia.pk, identificador= id_surtidor, estatus=True ).last()
            serial_final = Registroseriales.objects.filter(cia = cia.pk, identificador= id_surtidor, estatus=False ).last()
            datos_surtidor = Surtidores.objects.get(cia = cia.pk, id= id_surtidor)  

            
            guardar_cierre = Cierreseriales(serial_inicio = serial_inicial.serialfinal,fecha_incio=serial_inicial.creado, serial_final= serial_final.serialfinal )
            #guardar_cierre = Cierreseriales.objects.create(identificador=id_surtidor,  cia = cia.pk, , ,)
            guardar_cierre.identificador =  Surtidores.objects.get(id=id_surtidor)
            guardar_cierre.cia =  Companias.objects.get(usuario=request.user)
            guardar_cierre.usuario = request.user  
            guardar_cierre.totallitros =  serial_final.serialfinal - serial_inicial.serialfinal
            guardar_cierre.save()

            ejecutar_cierre = Registroseriales.objects.filter(cia = cia.pk, identificador= id_surtidor).update(estatus=True)
            cambiar_estado = Surtidores.objects.filter(cia = cia.pk, id = id_surtidor).update(cierre=False)                  
             
            #Insertar o Actualizar en el Cierre del dia
            cierrediario, created = CierreVentasDia.objects.get_or_create(producto=datos_surtidor.tipo, fecha_cierre=current_date, cia= Companias.objects.get(usuario=request.user), 
                                                                          usuario=request.user)
            if created:
                cierrediario.litros = 100
                cierrediario.precio = 0.50
                cierrediario.total = 50
                cierrediario.save()
                #messages.success(request, 'Cierre Ejecutado')  
                

            else:
                #messages.success(request, 'Cierre Actualizado')  
                cierrediario.litros = cierrediario.litros + 100
                cierrediario.total = cierrediario.litros * 0.50 
                cierrediario.save()
                       
            return render(request, 'cierreserial.html', {
            'seriales': seriales,
            'surtidores': surtidores,
            'mensaje': serial_final.serialfinal
            })
            
        except ValueError:        
            return render(request, 'cierreserial.html', {
            'seriales': seriales,
            'surtidores': surtidores

        } )       
            
                  
#Lista de Cierres Diarios            
def cierrediario(request):
    cia = Companias.objects.get(usuario=request.user)   
    lista = CierreVentasDia.objects.filter(cia = cia.pk)
    return render(request, 'listacierrediario.html', 
        { 'listas': lista  }              
    )     

def eliminarserial(request,id):
    registroserial = Registroseriales.objects.get(id=id)
    registroserial.delete()
    messages.success(request, 'Serial eliminado correctamente')  
    return redirect("/registroserialdiario/")
    
        
def listacierres(request):
    cia = Companias.objects.get(usuario=request.user)   
    cierres = Cierreseriales.objects.filter(cia = cia.pk).order_by('-id')
    return render(request, 'listacierres.html', 
        { 'cierres': cierres  }              
    )        

def compras(request):
    cia = Companias.objects.get(usuario=request.user)   
    lista_facturas = Facturas.objects.filter(cia = cia.pk)
    return render(request, 'compras.html', {'listas': lista_facturas} )        
        

def nuevafactura(request):
    cia = Companias.objects.get(usuario=request.user)  
    
    if request.method == 'GET':
        return render(request, 'nuevafactura.html', {
            'form' : FacturasForm

        } )      
    else:
        try:
            formulario = FacturasForm(request.POST)
            nuevo = formulario.save(commit=False)
            nuevo.usuario = request.user   
            nuevo.cia = Companias.objects.get(usuario=request.user)
            nuevo.save()
            messages.success(request, 'Registro guardado exitosamente')  

            return redirect('compras')
       
        except ValueError:  
            messages.warning(request, 'Registro no se pudo guardar')        
            return render(request, 'nuevafactura.html', {'form' : FacturasForm})               

def eliminarfactura(request,id):
    registro = Facturas.objects.get(id=id)
    registro.delete()
    messages.success(request, 'Registro eliminado correctamente')  
    return redirect("compras")

def editarfactura(request, id):
    cia = Companias.objects.get(usuario=request.user)  
    registro = Facturas.objects.get(id=id)
    form = FacturasForm(instance=registro) 

    if request.method == 'POST':
        try:
            form = FacturasForm(request.POST, instance=registro)           
            if form.is_valid():       
                form.save()
                messages.success(request, 'Registro guardado exitosamente')  
                return redirect('compras')
       
        except ValueError:  
            messages.warning(request, form.id)        
            return render(request, 'nuevafactura.html', {'form' : form})    
        
    return render(request, 'nuevafactura.html', {
        'form' : form

    } )      

  
def registrotanques(request):
    #today = datetime.date.today()
    cia = Companias.objects.get(usuario=request.user)   
    listas = RegistroTanques.objects.filter(cia = cia.pk ).order_by('-id')[:100]
        
    if request.method == 'POST':
        try: 
            #consulta medida de tanque
            litros = MedidasTanques.objects.get(cia=cia.pk, tanque=request.POST['tanque'], medida=request.POST['medida']).litros 
            reserva = Tanques.objects.get(cia=cia.pk, id=request.POST['tanque']).reserva_estrategica  

            form = RegistroTanquesForm(request.POST)     
            if form.is_valid(): 
                guardar = form.save(commit=False)
                guardar.usuario = request.user      
                guardar.cia = Companias.objects.get(usuario=request.user)    
                guardar.litros = litros  
                guardar.disponible =  litros - reserva

                guardar.save()
                messages.success(request, 'Registro guardado exitosamente')  
                return redirect('registrotanques')
       
        except ValueError:  
            messages.warning(request, form.id)        
            return render(request, 'nuevafactura.html', {'form' : form})    
        
    return render(request, 'registrotanques.html', 
        { 'form': RegistroTanquesForm, 
         'listas': listas  }              
    ) 
    
def eliminarregistrotanque(request,id):
    registro = RegistroTanques.objects.get(id=id)
    registro.delete()
    messages.success(request, 'Registro eliminado correctamente')  
    return redirect("registrotanques")

    
def volumentanques(request):    
    cia = Companias.objects.get(usuario=request.user)   
    listas = MedidasTanques.objects.filter(cia = cia.pk ).order_by('-medida')[:500]
    if request.method == 'POST':
        try: 
            #CONSULTAR SI YA EXISTE LA MEDIDA REGISTRADA PARA EL TANQUE
            verificar = MedidasTanques.objects.filter(cia=cia.pk, tanque=request.POST['tanque'], medida = request.POST['medida'])  
            if not verificar :
                #consulta medida de tanque
                form = VolumenTanquesForm(request.POST)     
                if form.is_valid(): 
                    guardar = form.save(commit=False)
                    guardar.usuario = request.user      
                    guardar.cia = Companias.objects.get(usuario=request.user)                    
                    guardar.save()
                    messages.success(request, 'Registro guardado exitosamente')  
                    return redirect('volumentanques')
            else: 
                messages.warning(request, 'Registro Duplicado')  

                
        except ValueError:  
            messages.warning(request, form.id)        
            return render(request, 'volumentanques', {'form' : VolumenTanquesForm})    
 

    
    return render(request, 'volumentanques.html',
                  {'form': VolumenTanquesForm,
                   'formbuscar' : BusVolumenTanquesForm,
                   'listas': listas }
                  )
 
def elivolumenmedida(request,id):
    registro = MedidasTanques.objects.get(id=id)
    registro.delete()
    messages.success(request, 'Registro eliminado correctamente')  
    return redirect("volumentanques")
 
 #asignacion automatica del volumen de un tanque
def autvolumenmedida(request):
    cia = Companias.objects.get(usuario=request.user)      
    tanque1 = MedidasTanques.objects.filter(cia = cia.pk, tanque=int(request.POST['tanque'] ))
    
    for listadoMedidas in tanque1:
        tanque2 = MedidasTanques()
        tanque2.cia = Companias.objects.get(usuario=request.user)  
        tanque2.usuario = request.user
        tanque2.tanque = Tanques.objects.get(id=request.POST['tanquedestino'])   
        tanque2.medida = listadoMedidas.medida
        tanque2.litros = listadoMedidas.litros
        tanque2.save()
        messages.success(request, 'Automatizacion completada')  
        
    return redirect("volumentanques")
    

#buscar medidas por tanque
def buscarmedidastanques(request):    
    cia = Companias.objects.get(usuario=request.user)   
    if request.method == 'POST': 
        listas = MedidasTanques.objects.filter(cia = cia.pk, tanque = request.POST['tanque'] ).order_by('-medida')[:500]
    else: 
        listas = MedidasTanques.objects.filter(cia = cia.pk ).order_by('-medida')[:500]
    
    return render(request, 'volumentanques.html',
                  {'form': VolumenTanquesForm,
                   'formbuscar' : BusVolumenTanquesForm,
                   'listas': listas }
                  )
    
   