import datetime
from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Choice, Question


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
  
def create_question(question_text, days, choice_texts=[]):
  """
    質問を `question_text` と投稿された日から作成する。現在より過去の時間で投稿したい場合は days= -days、
    未来の時間で投稿したい場合は対してはdays= +daysとする。
  """
  time = timezone.now() + datetime.timedelta(days=days)
  q = Question.objects.create(question_text=question_text, pub_date=time)
  # 選択肢がある場合とない場合で変数に格納した際返ってくるモデルが変わるから注意が必要
  # 選択肢があるとChoiceオブジェクトが変える。ないとQuestionオブジェクトになる。
  if choice_texts:
    for choice_text in choice_texts:
      return q.choice_set.create(choice_text=choice_text, votes=0)
  else:
    return q

class QuestionIndexViewTests(TestCase):
  def test_no_questions(self):
    # reverse('polls:index')でpollsのindexページURLを返している。それを利用してアクセスしている。
    response = self.client.get(reverse('polls:index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No polls are available")

    self.assertQuerysetEqual(response.context['latest_question_list'], [])

  def test_past_question(self):
    question = create_question(question_text="Past question.", days=-30, choice_texts=['game set'])
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(
      response.context['latest_question_list'],
      [question.question],
    )
  
  def test_future_question(self):
    create_question(question_text="Future question.", days=30, choice_texts=['game set'])
    response = self.client.get(reverse('polls:index'))
    self.assertContains(response, "No polls are available")
    self.assertQuerysetEqual(response.context['latest_question_list'], [])

  def test_future_question_and_past_question(self):
    # 片方だけ変数に入れるのはテストの合格条件を判別する際に過去質問が表示されているのを確認するため
    question = create_question(question_text="Past question.", days=-30, choice_texts=['game set'])
    create_question(question_text="Future question.", days=30, choice_texts=['game set'])
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(
      response.context['latest_question_list'],
      [question.question],
    )
  
  def test_two_past_question(self):
    question1 = create_question(question_text="Past question 1.", days=-30, choice_texts=['game set'])
    question2 = create_question(question_text="Past qustion 2.", days=-5, choice_texts=['game set'])
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(
      response.context['latest_question_list'], [question2.question, question1.question],
    )

  def test_choice_question(self):
    """
      Indexページで
      選択肢のある質問を表示する。
    """
    choice_question = create_question(question_text='Indexページでの選択肢のある質問', days=-1, choice_texts=['game set'])
    url = reverse('polls:index')
    response = self.client.get(url)
    self.assertContains(response, choice_question.question)
  
  def test_no_choice_question(self):
    """
      Indexページで
      選択肢がない質問は表示しない。
    """
    no_choice_question = create_question(question_text='Indexページでの選択肢のない質問', days=-1)
    url = reverse('polls:index')
    response = self.client.get(url)
    self.assertNotContains(response, no_choice_question)

class QuestionDataViewTests(TestCase):

  def test_future_question(self):
    """
      detail.htmlの未来の日付のページにアクセスする場合は404を表示する、
    """
    # 現在から5日後の質問を作成する
    future_question = create_question(question_text = '未来の質問', days=5)
    url = reverse('polls:detail', args=(future_question.id,))
    response = self.client.get(url)
    # 合格条件
    # ページにアクセスした際のステータスコードが404
    self.assertEqual(response.status_code, 404)

  def test_past_question(self):
    """
      Detailページ
      過去の質問の場合はページを表示する。
    """
    past_question = create_question(question_text='過去の質問', days=-5, choice_texts=['geme set'])
    url = reverse('polls:detail', args=(past_question.id,))
    response = self.client.get(url)
    # ページに過去の質問が含まれている。
    self.assertContains(response, past_question.question)
  
  def test_choice_question(self):
    """
      Detailページ
      選択肢のある質問を表示する。
    """
    choice_question = create_question(question_text='detailページでの選択肢がある質問', days=-1, choice_texts=['game set'])
    url = reverse('polls:detail', args=(choice_question.id,))
    response = self.client.get(url)
    self.assertContains(response, choice_question.choice_text)

  def test_no_choice_question(self):
    """
      選択肢がない質問は表示しない。
    """
    no_choice_question = create_question(question_text='detailページでの選択肢のない質問', days=-1)
    url = reverse('polls:detail', args=(no_choice_question.id,))
    response = self.client.get(url)
    self.assertEqual(response.status_code, 404)
