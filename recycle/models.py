from django.db import models
from django.conf import settings

class Recycle(models.Model):
    CATEGORY_CHOICES = [
        ('trash', '일반 쓰레기'),
        ('vinyl', '비닐류'),
        ('plastic', '플라스틱'),
        ('can', '병 * 캔류'),
        ('paper', '종이류'),
        ('food', '음식물 쓰레기'),
        ('clothing', '의류 수거함')
    ]
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)  # 항목의 이름
    description = models.TextField()  # 항목의 설명
    image = models.ImageField(upload_to='recycle_images/', blank=True, null=True)  # 항목의 이미지
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
  