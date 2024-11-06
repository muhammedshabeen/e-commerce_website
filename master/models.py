from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin, hook, AFTER_CREATE,AFTER_UPDATE,AFTER_SAVE
from django.utils.text import slugify
from core.utils import BaseContent

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(_('email address'), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default='Pending',max_length=20,choices=(
        ('Active','Active'),
        ('Inactive','Inactive'),
        ('Deleted','Deleted'),
        ('Pending','Pending')
    ))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    

class Category(BaseContent):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250,null=True,blank=True)
    image = models.ImageField(upload_to ='category_image')
    display_order = models.IntegerField()
    
    @hook(AFTER_CREATE)
    def save_slug_store(self, *args, **kwargs):
        value = str(self.title)+" "+str(self.id)
        self.slug_category = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
        
class VarientType(BaseContent):
    varient_name = models.CharField(max_length=255) 
    
    def __str__(self):
        return self.varient_name
    
class Varient_Values(BaseContent):
    varient_values = models.CharField(max_length=255)
    image = models.ImageField(upload_to='varient_values_color',null=True,blank=True)
    varient_type = models.ForeignKey(VarientType,related_name='varient_type',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.varient_values
    