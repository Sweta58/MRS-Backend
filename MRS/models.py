from django.db import models

class Result(models.Model):
    hashDigest = models.CharField(max_length=35)

    def __str__(self):
        return self.hashDigest