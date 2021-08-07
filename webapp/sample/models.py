from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from enumfields import EnumField
from enumfields import Enum

import os
import datetime

def get_avatar_full_path(instance, filename): 
    ext = filename.split('.')[-1]
    filename = '{0}.{1}'.format(instance.pk, ext)    
    return os.path.join("avatars", str(instance.pk), filename) 

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

class SystemUserRole(Enum):
    SYS_ADMIN       = "SYS_ADMIN"
    SYS_USER        = "SYS_USER"

class Common(models.Model):
    created_at  = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL,
                    null=True, db_index=True, editable=False,
                    on_delete=models.SET_NULL, related_name="%(class)s_created")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                    null=True, db_index=True, editable=False,
                    on_delete=models.SET_NULL, related_name="%(class)s_modified")

    class Meta:
        abstract = True
        app_label = "sample"

class Company(Common):
    name        = models.CharField(max_length=250, db_index=True, unique=True)
    email       = models.EmailField(db_index=True)
    phone       = models.CharField(max_length=20, blank=True, null=True)
    address_1   = models.CharField(max_length=250, blank=True, null=True)
    address_2   = models.CharField(max_length=250, blank=True, null=True)
    street      = models.CharField(max_length=250, blank=True, null=True)
    city        = models.CharField(max_length=250, blank=True, null=True)
    state       = models.CharField(max_length=250, blank=True, null=True)
    zipcode     = models.CharField(max_length=20, blank=True, null=True)
    country     = models.CharField(max_length=250, blank=True, null=True)
    logo_url    = models.TextField(blank=True, null=True)

    class Meta:
        app_label = "sample"

    def __str__(self):
        return "{}".format(self.name)

    @property
    def full_address(self):
        address_line = ""
        address_line += self.address_1 if self.address_1 else ""
        address_line += " {}".format(self.address_2) if self.address_2 else ""
        address_line += " {}".format(self.street) if self.street else ""
        address_line += " {}".format(self.city) if self.city else ""
        address_line += " {}".format(self.state) if self.state else ""
        address_line += " {}".format(self.country) if self.country else ""
        address_line += " {}".format(self.zipcode) if self.zipcode else ""
        return address_line

class User(Common, AbstractUser):
    email           = models.EmailField(_("email address"), unique=True)
    company         = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    system_role     = EnumField(SystemUserRole, default=SystemUserRole.SYS_USER, blank=True, null=True)
    registered      = models.BooleanField(default=False, db_index=True)
    avatar          = models.ImageField(upload_to=get_avatar_full_path, null=True, blank=True, default='avatars/default_avatar.png')

    adult           = models.BooleanField(default=False)

    bio_text        = models.CharField(max_length=120, null=True, blank=True)
    status_text     = models.CharField(max_length=120, null=True, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)

    gender          = models.CharField(max_length=1, choices=GENDER_CHOICES,null=False,blank=False,default='M')
    mobile          = models.CharField(max_length=15,null=True,blank=True)

    display_name    = models.CharField(max_length=128, blank=True, null=True)
    job_title       = models.CharField(max_length=250, blank=True, null=True)
    department      = models.CharField(max_length=250, blank=True, null=True)
    phone           = models.CharField(max_length=32, blank=True, null=True)
    address_1       = models.CharField(max_length=250, blank=True, null=True)
    address_2       = models.CharField(max_length=250, blank=True, null=True)
    street          = models.CharField(max_length=64, blank=True, null=True)
    city            = models.CharField(max_length=64, blank=True, null=True)
    state           = models.CharField(max_length=64, blank=True, null=True)
    zipcode         = models.CharField(max_length=32, blank=True, null=True)
    country         = models.CharField(max_length=64, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name', 'username'] 

    class Meta:
        app_label = "sample"

    def __str__(self):
        return '%s' % (self.email)

    @property
    def age(self):
        today = datetime.date.today()
        if self.date_of_birth is None:
            return 0
        rest = 1 if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day) else 0
        return today.year - self.date_of_birth.year - rest

    def is_adult(self):        
        if (datetime.date.today() - self.date_of_birth) > datetime.timedelta(days=18*365):
            self.adult = True

    def save(self, *args, **kwargs):
        if not self.date_of_birth is None:
            self.is_adult()

        super(User, self).save(*args, **kwargs)

    @property
    def full_address(self):
        address_line = ""
        address_line += self.address_1 if self.address_1 else ""
        address_line += " {}".format(self.address_2) if self.address_2 else ""
        address_line += " {}".format(self.street) if self.street else ""
        address_line += " {}".format(self.city) if self.city else ""
        address_line += " {}".format(self.state) if self.state else ""
        address_line += " {}".format(self.country) if self.country else ""
        address_line += " {}".format(self.zipcode) if self.zipcode else ""
        return address_line

