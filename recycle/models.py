from django.db import models
from django.conf import settings

class Recycle(models.Model):
    CATEGORY_CHOICES = [
        ('trash', '일반쓰레기'),
        ('vinyl', '비닐류'),
        ('plastic', '플라스틱'),
        ('can', '병*캔류'),
        ('paper', '종이류'),
        ('food', '음식물쓰레기'),
        ('clothing', '의류수거함'),
        ('others', '기타')
    ]
   
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100) 
    description = models.TextField() 
    image = models.ImageField(max_length=255, null=True, blank=True)
    tip = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.name
    
    @property
    def image_url(self):
        return f'recycle_images/{self.image}'

