from django.db import models
from django.conf import settings
from django.utils import timezone


class InteriorPost(models.Model):
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='interior_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 기본값 제거
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interior_likes', blank=True)
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interior_bookmarks', blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def total_bookmarks(self):
        return self.bookmarks.count()