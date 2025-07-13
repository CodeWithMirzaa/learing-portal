from django.db import models

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