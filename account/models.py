from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel

class Visitor(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    def __str__(self):
        return f"{self.user.username}"