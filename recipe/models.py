from django.db import models
from django.conf import settings
from django.urls import reverse

class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('korean', '한식'),
        ('chinese', '중식'),
        ('western', '양식'),
        ('japanese', '일식'),
        ('snack', '분식'),
        ('others', '기타'),
    ]

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
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="카테고리", default='others')
    image = models.ImageField(upload_to='recipes/', blank=True, null=True, verbose_name="레시피 이미지")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="작성자")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='recipe_likes', blank=True)
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='recipe_bookmarks', blank=True)

    def __str__(self):
        return self.recipe_name

    def get_absolute_url(self):
        return reverse('recipe_user:recipe_detail', args=[str(self.id)])

    class Meta:
        ordering = ['-created_at']

    def total_likes(self):
        return self.likes.count()

    def total_bookmarks(self):
        return self.bookmarks.count()
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='recipe_comments')
    recipe = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class UserChoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True)
    recipe_name = models.CharField(max_length=255, null=True, blank=True)  # CSV 항목에 대한 반응을 저장
    liked = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.recipe:
            return f"{self.user.username} - {self.recipe.recipe_name} - {'Liked' if self.liked else 'Disliked'}"
        else:
            return f"{self.user.username} - {self.recipe_name} - {'Liked' if self.liked else 'Disliked'}"