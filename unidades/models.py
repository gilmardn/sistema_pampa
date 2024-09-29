from django.db import models

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


    
class Filial(models.Model):
    nome = models.CharField(max_length=100)
    rua = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    numero = models.CharField(max_length=6)
    cidade = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=100)
    foto = models.ImageField(upload_to="fotos_perfil")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    

    def __str__(self):
        return self.nome
        
class Saldo(models.Model):
    data = models.DateField()
    tergrasa = models.IntegerField(default=0)
    termasa = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    filial = models.ForeignKey(Filial, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.filial.nome
    
    def data_formatada(self):
        return self.data.strftime('%d/%m/%y')
    
    