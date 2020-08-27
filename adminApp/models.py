from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import datetime
from django.utils import timezone
import datetime

# Create your models here.

class Profile(models.Model):
    gender = models.CharField(max_length=50, blank=True, null=True)
    # user = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE)
    user = models.OneToOneField(User, verbose_name='Author', related_name='author', on_delete=models.CASCADE, )
    date_created =  models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    def twenty_four(self):
        created_user = User.objects.count()
        diff = timezone.now() - datetime.timedelta(days=1)
        created = Profile.objects.filter(date_created__gte=diff)
        print('yeah')
        print(created)
        return created.count()
        
    def __str__(self):
        return self.gender

    class Meta:
        ordering = ['-id']

    


class ProfileDetails(Profile):
    class Meta:
        proxy = True
        verbose_name = 'User Metric'
