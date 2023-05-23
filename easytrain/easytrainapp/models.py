from django.db import models

class DataCollectionUrls(models.Model):
    word = models.CharField(max_length=255)
    urls =  models.CharField(max_length=10000)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.word