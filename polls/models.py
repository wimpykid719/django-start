from django.db import models

# Create your models here.
# 各モデルがmodels.Modelを継承して使っている。
# models.modelのサブクラスになる。
class Question(models.Model):
  # クラス変数を定義する。データベースフィールドを表現している。
  # Charフィールドは文字のフィールド
  question_text = models.CharField(max_length=200)

  # 日時のフィールド
  pub_date = models.DateTimeField('date published')

class Choice(models.Model):
  # これはChoiceがQuestionに関連付けられている事を伝えている。
  # データベースの多対一、多対多、一対一のようなデータベースリレーションシップに対応する。
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)