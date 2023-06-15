from django.db import models

class DataCollectionUrls(models.Model):
    word = models.CharField(max_length=255)
    urls =  models.CharField(max_length=10000)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.word
    
class PersonalaiKeys(models.Model):
    key = models.CharField(max_length=255)
    user = models.IntegerField()
    updated_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.key
    
class Profiles(models.Model):
    user = models.IntegerField()
    name = models.CharField(max_length=255)
    updated_time = models.DateTimeField(auto_now=True)
    PersonalaiKey = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True, null=False)
    
    def __str__(self):
        return self.name

class Packages(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    updated_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class ProfilePackages(models.Model):
    user = models.IntegerField()
    package = models.IntegerField()
    updated_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user