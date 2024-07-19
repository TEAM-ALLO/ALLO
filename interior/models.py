from django.db import models
from django.conf import settings
from django.utils import timezone

class InteriorPost(models.Model):
    CATEGORY_CHOICES = [
        ('modern', 'Modern'),
        ('classic', 'Classic'),
        ('industrial', 'Industrial'),
        ('scandinavian', 'Scandinavian'),
        ('bohemian', 'Bohemian'),
    ]

    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    image = models.ImageField(upload_to='interior_images/', verbose_name="인테리어 이미지")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interior_posts')  # 기본값 제거
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interior_likes', blank=True)
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interior_bookmarks', blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=None, null=True, blank=True, verbose_name="카테고리")
    furniture_list = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def total_bookmarks(self):
        return self.bookmarks.count()


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interior_comments')
    post = models.ForeignKey(InteriorPost, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
