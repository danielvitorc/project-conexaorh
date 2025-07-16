from django.db import models

class Filial(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Base(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, related_name='bases')  

    def __str__(self):
        return self.nome

class Setor(models.Model):
    nome = models.CharField(max_length=50)
    base = models.ForeignKey(Base, on_delete=models.CASCADE, related_name='setores')

    def __str__(self):
        return self.nome

class Curso(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Cargo(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    cursos = models.ManyToManyField(Curso, related_name='cargos')
    setores = models.ManyToManyField(Setor, related_name='cargos')

    def __str__(self):
        return self.nome

