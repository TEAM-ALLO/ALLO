from django.db import models
from django.conf import settings
from django.urls import reverse

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=100, verbose_name="레시피 이름")
    ingredients = models.TextField(verbose_name="재료")
    instructions = models.TextField(verbose_name="조리 방법")
    cooking_time = models.PositiveIntegerField(verbose_name="조리 시간(분)")
    servings = models.PositiveIntegerField(verbose_name="인분", default=1)
    difficulty = models.CharField(max_length=20, choices=[
        ('쉬움', '쉬움'),
        ('보통', '보통'),
        ('어려움', '어려움')
    ], verbose_name="난이도")
    image = models.ImageField(upload_to='recipes/', blank=True, null=True, verbose_name="레시피 이미지")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="작성자")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='recipe_likes', blank=True)
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='recipe_bookmarks', blank=True)

    def __str__(self):
        return self.recipe_name

    def get_absolute_url(self):
        return reverse('recipe_detail', args=[str(self.id)])

    class Meta:
        ordering = ['-created_at']

    def total_likes(self):
        return self.likes.count()

    def total_bookmarks(self):
        return self.bookmarks.count()
