from django.db import models
from account.models import CustomUser
from common.models import BaseModel

class UserProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    has_kyc = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email + ' Profile'
