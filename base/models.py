import random
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="created_%(class)s")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="updated_%(class)s")

    class Meta:
        abstract = True

class ResetCode(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f"Reset Code for {self.user.username}: {self.code}"

    @staticmethod
    def generate_reset_code(user):
        """Generates a 6-digit reset code, saves it to the database, and returns it."""
        code = ''.join(str(random.randint(0, 9)) for _ in range(6))  # Generates a 6-digit code
        reset_entry, created = ResetCode.objects.update_or_create(
            user=user,
            defaults={'code': code}
        )
        return code

