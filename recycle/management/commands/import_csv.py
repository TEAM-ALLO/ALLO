import csv
from typing import Any
from django.core.management.base import BaseCommand
import os
from recycle.models import Recycle
from users.models import User

class Command(BaseCommand):
    help = 'Import ALLO CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='CSV file path')
        
    def handle(self, *args, **kwargs):
        superuser = User.objects.filter(is_superuser=True).first()
        if not superuser:
            self.stdout.write(self.style.ERROR('No superuser found'))
            return
        
        csv_file_path = kwargs['csv_file_path']
        
        if not os.path.isfile(csv_file_path):
            self.stdout.write(self.style.ERROR("File does not exist"))
            return
        
        # 기존 데이터를 삭제
        Recycle.objects.all().delete()

        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                Recycle.objects.create(
                    category=row.get('category', ''),
                    name=row['name'],
                    description=row.get('description', ''),
                    image=row.get('image', ''),
                    tip=row.get('tip', ''),
                    author=superuser  # author 필드 설정
                )

        self.stdout.write(self.style.SUCCESS("Data imported successfully"))
