from django.db import models

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=255, unique=True)
    pub_date = models.DateTimeField()
    content = models.TextField()

    def __str__(self):
        return self.title
