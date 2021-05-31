from django.contrib import admin
from django.db.models.query_utils import Q
from .models import Question, Choice
# Register your models here.

# class ChoiceInline(admin.StackedInline):

# 上記の場合画面を占領が大きいので、コンパクトにする。
class ChoiceInline(admin.TabularInline):
  model = Choice
  # ここで指定した数だけ、Choiceオブジェクトの項目が表示される。
  # 3の場合新たに3つ選択肢を追加できる。
  extra = 3

# question_textとpub_dateの表示される順番を入れ替える。
class QuestionAdmin(admin.ModelAdmin):
  # fields = ['pub_date', 'question_text']
  # これでquestion_textとoub_dateが分けられて表示される。
  # pub_dateの上部に Date 詳細です。と分ける要素が追加される。
  list_display = ('question_text', 'pub_date', 'was_published_recently')
  # 日付で絞れる。
  list_filter = ['pub_date']
  # 質問を検索できるようになる。
  search_fields = ['question_text']

  fieldsets = [
    (None, {'fields': ['question_text']}),
    ('Date 詳細です。', {'fields': ['pub_date'], 'classes': ['collapse']}),
  ]
  # 作成したChoiceInlineクラスを読み込む
  # これでChoiceオブジェクトをQuestionの管理ページから編集する事ができる。
  inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)

#admin.site.register(Choice)