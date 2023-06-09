from django import forms
from django.forms import ModelForm
from .models import Registroseriales, Facturas, RegistroTanques
 
class RegistroserialesForm(ModelForm):
    class Meta: 
        model = Registroseriales
        fields = ['identificador','serialfinal', 'observaciones']
        labels = {
            "identificador": ("SURTIDOR"),
            "serialfinal": ("SERIAL FINAL"),
            "observaciones": ("OBSERVACIONES")
        }
        widgets = {
            'identificador': forms.Select(attrs={'class':'form-control'}),
            'serialfinal': forms.TextInput(attrs={'class':'form-control'}),
            'observaciones': forms.TextInput(attrs={'class':'form-control'})
        }
 
class FacturasForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_recibido'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields['fecha_emision'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        
        self.fields['fecha_pago'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
    class Meta: 
        model = Facturas
        fields = ['numero_factura','fecha_recibido', 'fecha_emision','conductor', 'placa_cisterna','planta_distribucion','cant_bruta', 'cant_neta','monto_pagar','fecha_pago','referencia_pago', 'estatus_pago']
        labels = {
            "numero_factura": ("FACTURA"),
            "fecha_recibido": ("FECHA RECIBIDO"),
            "fecha_emision": ("FECHA EMISION"),
            "conductor": ("CONDUCTOR"),
            "placa_cisterna": ("PLACA CISTERNA"),
            "planta_distribucion": ("PLANTA"),
            "cant_bruta": ("CANT. BRUTA"),
            "cant_neta": ("CANT. NETA"),
            "monto_pagar": ("MONTO A PAGAR"),
            "fecha_pago": ("FECHA PAGO"),
            "referencia_pago": ("REF. PAGO"),
            "estatus_pago": ("ESTATUS PAGO"),
            
        }
        widgets = {
            'numero_factura': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_recibido': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_emision': forms.TextInput(attrs={'class':'form-control'}),
            'conductor': forms.TextInput(attrs={'class':'form-control'}),
            'placa_cisterna': forms.TextInput(attrs={'class':'form-control'}),
            'planta_distribucion': forms.TextInput(attrs={'class':'form-control'}),
            'cant_bruta': forms.TextInput(attrs={'class':'form-control'}),
            'cant_neta': forms.TextInput(attrs={'class':'form-control'}),
            'monto_pagar': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_pago': forms.TextInput(attrs={'class':'form-control'}),
            'referencia_pago': forms.TextInput(attrs={'class':'form-control'}),
                'estatus_pago': forms.CheckboxInput(
                    attrs={
                        'class':'form-check-input form-check',
                    }
                ),
        }
 
class RegistroTanquesForm(ModelForm):
    class Meta: 
        model = RegistroTanques
        fields = ['tanque','medida', 'observacion']
        labels = {
            "tanque": ("TANQUE"),
            "medida": ("MEDIDA CM"),
            "observacion": ("OBSERVACIONES")
        }
        widgets = {
            'tanque': forms.Select(attrs={'class':'form-control'}),
            'medida': forms.TextInput(attrs={'class':'form-control'}),
            'observacion': forms.TextInput(attrs={'class':'form-control'})
        }   


   
        
        
