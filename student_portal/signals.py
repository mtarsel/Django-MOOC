from django.db.models.signals import post_save

post_save.connect(create_profile, sender=User)
