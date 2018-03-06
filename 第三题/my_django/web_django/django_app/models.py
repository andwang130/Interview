from django.db import models

# Create your models here.
class User(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=25)
    paswd=models.CharField(max_length=25)
    emila=models.EmailField()
    set_time=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'user'
class AdminU(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    paswd = models.CharField(max_length=25)
    set_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'adminu'
class ArticleType(models.Model):
    id=models.AutoField(primary_key=True)
    typename=models.CharField(max_length=25)
    set_time=models.DateTimeField(auto_now_add=True)
class Article(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=25)
    conten=models.TextField()
    type=models.ForeignKey(ArticleType,on_delete=models.CASCADE)
    authon=models.ForeignKey(AdminU,on_delete=models.CASCADE)
    set_time=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'article'
class Comment(models.Model):
    id=models.AutoField(primary_key=True)
    conten=models.CharField(max_length=500)
    publisher=models.ForeignKey(User,on_delete=models.CASCADE)
    article=models.ForeignKey(Article,on_delete=models.CASCADE)
    set_time=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'comment'
