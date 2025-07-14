from django.contrib import admin
from .models import Choice, Product, QuizQuestion, Video


admin.site.register(Product)
admin.site.register(Video)

admin.site.register(QuizQuestion)
admin.site.register(Choice)