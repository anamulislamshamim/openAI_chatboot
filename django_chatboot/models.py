from django.db import models
from django.contrib.auth.models import User 


class Chatboot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username}: {self.message}'
