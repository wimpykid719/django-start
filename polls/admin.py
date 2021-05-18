from django.contrib import admin
from django.db.models.query_utils import Q
from .models import Question
# Register your models here.

admin.site.register(Question)