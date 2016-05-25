from django.db import models

# Create your models here.
class Commit(models.Model):
    nama_project = models.CharField(max_length=30)
    hashnya = models.CharField(max_length=20)
    commiter = models.CharField(max_length=20)
    message = models.TextField()
    generated_comment = models.TextField()

class Files(models.Model):
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE)
    filename = models.TextField()
    status = models.CharField(max_length=20)
    perubahan = models.TextField()
