import os
from django.conf import settings
from django.core.management.base import BaseCommand
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import pickle
from recipe.models import Recipe

class Command(BaseCommand):
    help = 'Train the recipe recommendation model'

    def handle(self, *args, **kwargs):
        # CSV 파일 경로 설정
        file_path_1 = os.path.join(settings.BASE_DIR, 'TB_RECIPE_SEARCH-220701.csv')
        file_path_2 = os.path.join(settings.BASE_DIR, 'TB_RECIPE_SEARCH-20231130.csv')

        # CSV 파일 로드
        df1 = pd.read_csv(file_path_1)
        df2 = pd.read_csv(file_path_2)

        # C열에 해당하는 요리 이름 추출
        recipe_names_1 = df1.iloc[:, 2].dropna().unique()  # C열 (0-index라서 2)
        recipe_names_2 = df2.iloc[:, 2].dropna().unique()

        # 두 파일의 요리 이름 합치기
        recipe_names = list(set(recipe_names_1).union(set(recipe_names_2)))

        # 요리 이름을 Recipe 모델에 저장
        for name in recipe_names:
            if not Recipe.objects.filter(recipe_name=name).exists():
                Recipe.objects.create(recipe_name=name)


        try:
            # 데이터 불러오기 및 모델 훈련
            recipes = Recipe.objects.all().values('id', 'recipe_name', 'ingredients', 'instructions')
            df = pd.DataFrame(recipes)

            # 텍스트 결합
            df['combined_features'] = df['recipe_name'] + " " + df['ingredients'] + " " + df['instructions']

            # CountVectorizer 객체 생성 및 훈련
            vectorizer = CountVectorizer()
            count_matrix = vectorizer.fit_transform(df['combined_features'])

            # 파일 경로 설정
            vectorizer_path = os.path.join(settings.BASE_DIR, 'count_vectorizer.pkl')
            df_path = os.path.join(settings.BASE_DIR, 'recipes_df.pkl')

            # CountVectorizer 객체 저장
            with open(vectorizer_path, 'wb') as f:
                pickle.dump(vectorizer, f)

            # 데이터프레임 저장
            with open(df_path, 'wb') as f:
                pickle.dump(df, f)

            self.stdout.write(self.style.SUCCESS('Model trained and saved successfully'))

            # 파일이 제대로 저장되었는지 확인하기 위해 읽어오기 시도
            with open(vectorizer_path, 'rb') as f:
                vectorizer_loaded = pickle.load(f)
            with open(df_path, 'rb') as f:
                df_loaded = pickle.load(f)

            self.stdout.write(self.style.SUCCESS('Model loaded successfully for verification'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
