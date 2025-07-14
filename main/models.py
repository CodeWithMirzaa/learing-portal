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
    
    

class Video(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=100)
    youtube_url = models.URLField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.title} – {self.title}"

    def youtube_id(self):
        """
        Extracts YouTube video ID from various possible URL formats.
        """
        regex = (
            r'(?:youtube\.com/(?:watch\?v=|embed/)|youtu\.be/)([^\s&?/]+)'
        )
        match = re.search(regex, self.youtube_url)
        return match.group(1) if match else ''
