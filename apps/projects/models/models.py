from django.db import models


class Project(models.Model):
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']