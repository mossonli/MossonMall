from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


User = get_user_model()
"""
post_save 属于model signal sent at the end of the save() method.
注意，如果信号没有被处罚，在settings的NSTALLED_APPS里不要用users添加，换成users.apps.UsersConfig
"""


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    print("created", created)
    if created:
        print("signals register")
        password = instance.password
        instance.set_password(password)
        instance.save()
