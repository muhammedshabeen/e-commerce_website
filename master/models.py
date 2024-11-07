from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin, hook, AFTER_CREATE,AFTER_UPDATE,AFTER_SAVE
from django.utils.text import slugify
from core.utils import BaseContent
from taggit.managers import TaggableManager


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
    
class VarientValues(BaseContent):
    varient_values = models.CharField(max_length=255)
    image = models.ImageField(upload_to='varient_values_color',null=True,blank=True)
    varient_type = models.ForeignKey(VarientType,related_name='varient_type',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.varient_values

class ProductVarients(LifecycleModelMixin,models.Model):
    slug_product_varient = models.SlugField(max_length=500,blank=True,null=True)
    multivarient_values = models.ForeignKey(VarientValues,related_name='multivarient_values',on_delete=models.CASCADE,null=True,blank=True)
    Varient_Values = models.ForeignKey(VarientValues,related_name='primary_values',on_delete=models.CASCADE)
    Selling_Prize = models.DecimalField(max_digits=12,decimal_places=3)
    Display_Prize = models.DecimalField(max_digits=12,decimal_places=3)
    meta_title = models.CharField(max_length=256,null=True,blank=True)
    meta_description = models.TextField(blank=True,null=True)
    meta_div =models.TextField(blank=True,null=True)
    Product_stock = models.PositiveIntegerField(blank=True,null=True)
    sku_code = models.CharField(max_length=100,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default='Active',max_length=20, choices=(
        ('Active','Active'),
        ('Pending','Pending'),
        ('Suspended','Suspended'),
    ))
    
    # def __str__(self) -> str:
    #     if self.Varient_Values.Varient_Values == "Nill":
    #         return str(self.products.first())
    #     else:
    #         return f"{self.products.first()}({self.Varient_Values.Varient_Values})"
    
        
class VarientProductImages(models.Model):
    parent_varient = models.ForeignKey(ProductVarients,on_delete=models.CASCADE,related_name='varient_image',null=True)
    Images = models.FileField(upload_to='product_images')
    display_order = models.IntegerField()

class Product(models.Model):
    Name = models.CharField(max_length=250)
    Last_name = models.CharField(max_length=250,blank=True)
    Description = models.TextField()
    thumbnail_image = models.FileField(upload_to='product_thumbnail',null=True,blank=True)
    single_varient = models.ForeignKey(VarientType,related_name="varient_typel",on_delete=models.CASCADE)
    multivarient = models.ForeignKey('master.VarientType',related_name="multivarient_ll", on_delete=models.CASCADE,null=True,blank=True)
    Product_Category = models.ForeignKey(Category,related_name="category_products",on_delete=models.CASCADE,null=True,blank=True)
    Product_Items = models.ManyToManyField(ProductVarients,related_name='products',verbose_name='ProductItems',blank=True)
    related_products = models.ManyToManyField('Product',blank=True)
    return_eligibility = models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No')),default='No')
    coming_soon = models.CharField(max_length=50,choices=(('Yes','Yes'),('No','No')),default='No')
    status = models.CharField(default='Not verified',max_length=20, choices=(
        ('Active','Active'),
        ('Not verified','Not verified'),
        ('Suspended','Suspended'),
    ))
    order_payment_status = models.CharField(default='Both',max_length=20, choices=(
        ('Online','Online'),
        ('Cod','Cod'),
        ('Both','Both'),
    ))
    update_within = models.IntegerField(blank=True,null=True)
    updated_on = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    display_order = models.IntegerField(blank=True,null=True)
    note = models.TextField(blank=True,null=True)
    
    tags = TaggableManager()

    def __str__(self) -> str:
        return self.Name


class AddressTable(models.Model):
    customer = models.ForeignKey(get_user_model(),related_name="address", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100,null=True,blank=True)
    pincode = models.CharField(max_length=20,null=True,blank=True)
    block = models.CharField(max_length=255,null=True,blank=True)
    street = models.CharField(max_length=100,null=True,blank=True)
    avenue = models.CharField(max_length=255,null=True,blank=True)
    housename = models.CharField(max_length=255,null=True,blank=True)
    remark = models.CharField(max_length=255,null=True,blank=True) 
    phone = models.CharField(max_length=100,null=True,blank=True)
    is_default = models.BooleanField(default=False)
    status = models.BooleanField(default=True,max_length=20, choices=(
        (True,'Active'),
        (False,'Pending'),
    ))
    
    def __str__(self) -> str:
        return self.name + " address"

    
    
    

class Order(LifecycleModelMixin,models.Model):
    user = models.ForeignKey(get_user_model(),related_name="customer_order",on_delete=models.CASCADE)
    order_id_m = models.CharField(unique=True,max_length=200)
    order_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    delivery_charge = models.IntegerField(default=0)
    order_total = models.DecimalField(max_digits=20,decimal_places=3)
    discount = models.IntegerField(null=True,blank=True)
    promocode_discound = models.CharField(max_length=100,null=True,blank=True)
    reward_point_discound = models.CharField(max_length=100,null=True,blank=True)
    address = models.TextField()
    type = models.CharField(max_length=100,choices=(('own','own'),('partner','partner')),default='own')
    partner_id = models.CharField(max_length=100,null=True,blank=True)
    cancelled_by = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True,blank=True)
    order_status = models.CharField(max_length=20,choices=(
        ('Ordered','Ordered'),
        ('failed','Failed'),
        ('processing','Processing'),
        ('shipped','Shipped'),
        ('out for delivery','Out for delivery'),
        ('delivered','Delivered'),
        ('cancelled','Cancelled'),
    ),default='Ordered')
    payment_status = models.CharField(max_length=20,choices=(
        ('Pending','Pending'),
        ('Received','Received'),
        ('Failed','Failed'),
        
    ),default='Pending')
    supplier = models.CharField(max_length=255,null=True,blank=True)
    platform = models.CharField(max_length=100,null=True,blank=True,default=0)
    mode = models.CharField(max_length=100,blank=True)
    order_response = models.JSONField(null=True,blank=True)
    order_type = models.CharField(max_length=20,choices=(
        ('request_friend','request_friend'),
        ('normal','normal'),
    ),default='normal')

    
    
class OrderDetails(models.Model):
    order_id = models.ForeignKey(Order,related_name='products',on_delete=models.CASCADE)
    customer = models.ForeignKey(get_user_model(), related_name="order_customer",on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVarients,related_name='order_detail',on_delete=models.CASCADE)
    product_name = models.CharField(max_length=555,null=True)
    product_selling_price = models.DecimalField(max_digits=20,decimal_places=3,null=True,blank=True)
    product_display_price = models.DecimalField(max_digits=20,decimal_places=3,null=True,blank=True)
    product_quantity = models.IntegerField(null=True)
    product_varinet_name = models.CharField(max_length=255,null=True)
    product_multivarient_name = models.CharField(max_length=266,null=True)
    product_sku = models.CharField(max_length=255,null=True)
    amount = models.DecimalField(max_digits=12,decimal_places=3)
    amount_percentage = models.DecimalField(null=True,blank=True,max_digits=12,decimal_places=3)
    count = models.IntegerField()
    order_date = models.DateField(auto_now_add=True)
    order_time = models.TimeField(auto_now_add=True)
    discount = models.IntegerField(default=0)
    serial_number = models.CharField(max_length=512,blank=True,null=True)