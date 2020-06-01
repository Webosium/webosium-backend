from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CommonModelFields(models.Model):
    archived   = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self):
        self.archived = True
        super().save()

    class Meta:
        abstract = True


class Tag(CommonModelFields):
    name = models.CharField(max_length=100, null=False, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.SET(1))

    def __str__(self):
        return self.name



STATUS = [
    ("D", "Draft"),
    ("P", "Pending"),
    ("A", "Approved"),
    ("R", "Rejected"),
]

class Event(CommonModelFields):
    name        = models.CharField(max_length=150, null=False, blank=False)
    link        = models.CharField(max_length=200, null=False, blank=False)
    date        = models.DateTimeField()
    timezone    = models.CharField(max_length=3, default='IST')
    description = models.TextField(null=True)
    tags        = models.ManyToManyField('Tag')
    image       = models.ImageField(upload_to='images/', null=True)
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE)
    status      = models.CharField(max_length=1, choices=STATUS, null=False, default='P')

    def __str__(self):
        return self.name
