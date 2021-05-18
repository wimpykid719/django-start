import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
# 各モデルがmodels.Modelを継承して使っている。
# models.modelのサブクラスになる。
class Question(models.Model):
  # クラス変数を定義する。データベースフィールドを表現している。
  # Charフィールドは文字のフィールド
  question_text = models.CharField(max_length=200)

  # 日時のフィールド
  pub_date = models.DateTimeField('date published')

  def __str__(self):
    # インスタンスを生成して、printした際にここが実行される。
    return self.question_text
  
  def was_published_recently(self):
    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):

  # これはChoiceがQuestionに関連付けられている事を伝えている。
  # データベースの多対一、多対多、一対一のようなデータベースリレーションシップに対応する。
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)

  def __str__(self):
    return self.choice_text