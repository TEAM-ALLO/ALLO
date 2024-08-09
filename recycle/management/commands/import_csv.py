import csv
from typing import Any
from django.core.management.base import BaseCommand
import os
from django.core.files import File
from recycle.models import Recycle
from users.models import User
# csv 파일로 변환된 골프장 정보들을 DB에 migrate하는 과정을 자동화
# 장고의 custom command 기능 -> 내가 임의로 만들고 싶은 명령어를 만들 수 있음

# 커스텀 커맨드의 클래스는 항상 BaseCommand를 상속 받는 command
class Command(BaseCommand):
    help = 'Import Park Golf CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('ourtrash.csv',type=str, help='CSV file path')
        
    def handle(self, *args, **kwargs):
        superuser = User.objects.filter(is_superuser=True).first()
        if not superuser:
            self.stdout.write(self.style.ERROR('No superuser found'))
            return
        
        csv_file_path = kwargs['ourtrash.csv']
        
        if not os.path.isfile(csv_file_path):
            self.stdout.write(self.style.ERROR("File does not exist"))
            return
        
        with open (csv_file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                Recycle.objects.create(
                    category=row.get('category', ''),
                    name=row['name'],
                    description=row.get('description', ''),
                    image=row.get('image', ''),
                )