from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Companias(models.Model):
    nombre = models.CharField(max_length=100)
    rif = models.CharField(max_length=10, null=True)
    direccion = models.TextField(blank=True)
    telefono = models.CharField(max_length=11)
    email = models.EmailField()
    representante = models.CharField(max_length=50)
    estatus = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre + '-' + self.rif + '-' + self.direccion
    
class Surtidores(models.Model):
    identificador =  models.CharField(max_length=6)
    tipo =  models.CharField(max_length=1) 
    serial_inicial = models.IntegerField()
    serial_actual = models.IntegerField(null=True)
    estatus = models.BooleanField(default=True)
    cierre = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now=True)
    cia = models.ForeignKey(Companias, related_name="compania", blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.identificador 

class Registroseriales(models.Model):
    identificador =  models.ForeignKey(Surtidores, blank=True, null=True, on_delete=models.CASCADE)
    cia = models.ForeignKey(Companias, blank=True, null=True, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    serialinicio = models.IntegerField(default=0)
    serialfinal = models.IntegerField(default=0)    
    totallitros = models.IntegerField(default= 0)    
    estatus = models.BooleanField(default=False)
    observaciones = models.CharField(max_length=300, null=True)

    
    def __str__(self):
        return str(self.identificador) + ' - ' + self.creado.strftime("%d-%b-%y %H:%M  ") + ' - ' + str(self.serialinicio) + ' - ' + str(self.serialfinal)
    
class Cierreseriales(models.Model): 
    identificador =  models.ForeignKey(Surtidores, blank=True, null=True, on_delete=models.CASCADE)
    cia = models.ForeignKey(Companias, blank=True, null=True, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    serial_inicio = models.IntegerField()
    fecha_incio = models.DateTimeField(null=True)
    serial_final = models.IntegerField()
    fecha_final = models.DateTimeField(auto_now=True)
    totallitros = models.IntegerField(default= 0)    
    estatus = models.BooleanField(default=False)

class Facturas(models.Model): 
    cia = models.ForeignKey(Companias, blank=True, null=True, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    numero_factura =  models.IntegerField(unique=True)
    fecha_recibido =  models.DateField()
    fecha_emision =  models.DateField()
    conductor = models.CharField(max_length=50)
    placa_cisterna = models.CharField(max_length=10)
    planta_distribucion = models.CharField(max_length=20)
    cant_bruta = models.FloatField()
    cant_neta = models.FloatField()
    monto_pagar = models.FloatField()
    estatus_pago = models.BooleanField(default=False)
    fecha_pago =  models.DateField(null=True)
    referencia_pago = models.CharField(max_length=15, null=True) 
    estatus = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.numero_factura) 


class Tanques(models.Model):
    cia = models.ForeignKey(Companias, blank=True, null=True, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_combustible = models.CharField(max_length=1, null=True)
    capacidad = models.IntegerField(default= 0)
    activo =  models.BooleanField(default=True)
    reserva_estrategica = models.IntegerField(default= 0)

    def __str__(self):
        return str(self.id)  +'-'+ str(self.capacidad)+'-'+ self.tipo_combustible
    
 
class RegistroTanques(models.Model):
    cia = models.ForeignKey(Companias, blank=True, null=True, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tanque = models.ForeignKey(Tanques, blank=True, null=True, on_delete=models.CASCADE)
    medida = models.IntegerField(default= 0)
    litros = models.IntegerField(default= 0)
    disponible = models.IntegerField(default= 0)
    observacion = models.CharField(max_length=30, null=True)
    
  
class MedidasTanques(models.Model):
    cia = models.ForeignKey(Companias, blank=True, null=True, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tanque = models.ForeignKey(Tanques, blank=True, null=True, on_delete=models.CASCADE)
    medida = models.IntegerField(default= 0)
    litros = models.IntegerField(default= 0)
    
class Aplicaciones(models.Model):
    nombre_app =  models.CharField(max_length=30)
    descripcion =  models.CharField(max_length=50)
    estatus = models.BooleanField(default=True)
    url = models.CharField(max_length=30)
    

  