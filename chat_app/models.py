from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Userprofile(user=instance)
        user_profile.save()
        user_profile.following.add(instance.userprofile)
        user_profile.save()

class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False,
        blank=True
    )
    user_online_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username