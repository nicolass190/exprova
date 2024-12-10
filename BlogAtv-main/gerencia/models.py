from django.db import models
from usuarios.models import UserBlog

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True, null=False, blank=False)
    
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name_plural = 'Categorias', 
        ordering = ['nome']
    

class Noticia(models.Model):
    titulo = models.CharField(max_length=100)
    data_publicacao = models.DateField(auto_created=True)
    texto = models.TextField()
    image = models.ImageField(upload_to='noticias/')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    usuario = models.ForeignKey( UserBlog, on_delete=models.CASCADE, blank=True,null=True)  
    

    