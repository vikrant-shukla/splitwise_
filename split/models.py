from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class SplitAmount(models.Model):
    owe_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owe_by")
    owe_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owe_from")
    owe_amount = models.DecimalField(decimal_places=2, max_digits=8)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("owe_by", "owe_from")
