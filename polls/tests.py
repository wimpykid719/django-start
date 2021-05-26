import datetime
from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question


# テストコードの書き方はTestCaseを継承する事
# メソッド名をtestから始める事でDjango側で実行してくれるようになる。

class QuestionModelTests(TestCase):
  def test_was_published_recently_with_future_question(self):
    """
      was_published_recently()はpub_dateが未来の場合Falseを返す。
    """

    time = timezone.now() + datetime.timedelta(days=30)
    future_question = Question(pub_date=time)

    self.assertIs(future_question.was_published_recently(), False)

  def test_was_published_recently_with_recent_question(self):
    """
      was_published_recently()はpub_dateが昨日までに投稿されたものなら　Trueを返す。
    """
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_question = Question(pub_date=time)

    self.assertIs(recent_question.was_published_recently(), True)
  
def create_question(question_text, days):
  """
    質問を `question_text` と投稿された日から作成する。現在より過去の時間で投稿しようとするとFlaseに、まだ公開されていない質問に対してはTrueを返す。
  """
  time = timezone.now() + datetime.timedelta(days=days)
  return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
  def test_no_questions(self):
    # reverse('polls:index')でpollsのindexページURLを返している。それを利用してアクセスしている。
    response = self.client.get(reverse('polls:index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No polls are available.")

    self.assertQuerysetEqual(response.context['latest_question_list'], [])

  def test_past_question(self):
    question = create_question(question_text="Past question.", days=-30)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(
      response.context['latest_question_list'],
      [question],
    )
  
  def test_future_question(self):
    create_question(question_text="Future question.", days=30)
    response = self.client.get(reverse('polls:index'))
    self.assertContains(response, "No polls are available.")
    self.assertQuerysetEqual(response.context['latest_question_list'], [])

  def test_future_question_and_past_question(self):
    # 片方だけ変数に入れるのはテストの合格条件を判別する際に過去質問が表示されているのを確認するため
    question = create_question(question_text="Past question.", days=-30)
    create_question(question_text="Future question.", days=30)
    print(question)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(
      response.context['latest_question_list'],
      [question],
    )
  
  def test_two_past_question(self):
    question1 = create_question(question_text="Past question 1.", days=-30)
    question2 = create_question(question_text="Past qustion 2.", days=-5)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(
      response.context['latest_question_list'], [question2, question1],
    )



    
