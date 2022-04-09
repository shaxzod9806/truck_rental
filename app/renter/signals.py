# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from index.models import User
# from .models import Profile
#
#
# # there should be filter to filter only renters
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.user_type == 3:
#             Profile.objects.create(user=instance)
