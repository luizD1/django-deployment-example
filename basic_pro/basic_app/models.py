from django.db import models
from django.contrib.auth.models import User
# from django.core.validators import ValidationError
# Create your models here.

# def url(value):
#     if value[0].lower() != 'z':
#         raise models.validationError('email must contain www')

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,
                               on_delete=models.CASCADE)

    # additional
    portfolio_site = models.URLField(blank=True,
                                    )

    profile_pic = models.ImageField(upload_to='profile_pics',
                                    blank=True)

    def __str__(self):
        return self.user.username
    
