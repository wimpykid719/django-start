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
    # シェルで表示されるオブジェクトに質問名が使われるだけでなく
    # adminでオブジェクトを表現する際にも使用されるので追加する必要がある。
    return self.question_text
  
  def was_published_recently(self):
    now = timezone.now()
    # now - datetime.timedelta(days=1)は今の時間から一日引いた日付を出す。
    # 2021-05-19 23:29:56.216634こんな感じの値になる。
    # pub_dateが現在時刻より過去で現在時刻から一日以内の場合はTrueを返すメソッド
    return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):

  # これはChoiceがQuestionに関連付けられている事を伝えている。
  # データベースの多対一、多対多、一対一のようなデータベースリレーションシップに対応する。
  # Question ← → Choiseと双方向のやりとりが可能となる。
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)

  def __str__(self):
    return self.choice_text