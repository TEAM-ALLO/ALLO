# Generated by Django 4.2.14 on 2024-08-20 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interior', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interiorpost',
            name='category',
            field=models.CharField(blank=True, choices=[('modern', '모던'), ('european', '유럽풍'), ('classic', '클래식'), ('natural', '내추럴'), ('colorful', '컬러풀'), ('other', '기타')], default=None, max_length=50, null=True, verbose_name='카테고리'),
        ),
    ]
