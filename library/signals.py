from django.db.models.signals import post_save  # signalas (būna įvairių)
from django.contrib.auth.models import User  # siuntėjas
from django.dispatch import receiver  # priėmėjas (dekoratorius)
from .models import Profile


# When user is created we are creating profile too
@receiver(post_save, sender=User)  # if user object is saved, we initialise function after decorator
def create_profile(sender, instance, created, **kwargs):  # instance is just created user.
    """ Create a profile if a User instance was created
    If the User object is saved, this function get called
    :param sender: User model class
    :param instance: created specific instance of Profile
    :param created: boolean whether User was created
    :param kwargs:
    """
    if created:
        Profile.objects.create(user=instance)
        print('KWARGS: ', kwargs)


# If we edit user, we save profile too
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
