from django.db import models


import re

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Video(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=100)
    youtube_url = models.URLField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.title} – {self.title}"

    def youtube_id(self):
        regex = r'(?:youtube\.com/(?:watch\?v=|embed/)|youtu\.be/)([^\s&?/]+)'
        match = re.search(regex, self.youtube_url)
        return match.group(1) if match else ''


class QuizQuestion(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)
    option_d = models.CharField(max_length=100)
    correct_option = models.CharField(max_length=1, choices=[
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')
    ])

    def __str__(self):
        return f"{self.question_text} (Video: {self.video.title})"


class Choice(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
