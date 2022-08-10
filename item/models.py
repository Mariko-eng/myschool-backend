from django.db import models
from django.core.files import File
from io import BytesIO
from PIL import Image
from django.contrib.auth.models import User
from mulumba.utils import random_string_generator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

class Category(models.Model):
    cat_code = models.CharField(max_length=200,unique=True)
    name = models.CharField(max_length=200,unique=True)

    def get_category_total(self):
        items = self.item_set.all()
        total = 0
        for i in items:
            total = total + i.get_inward_stock_total()
        return total
    
    def __str__(self) -> str:
        return self.name

class Item(models.Model):
    item_code = models.CharField(max_length=200,unique=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200,unique=True)
    description = models.TextField(null=True,blank=True,help_text="Short Description Of the Product")
    initail_measure = models.CharField(max_length=200, null=True,blank=True)
    initail_price = models.DecimalField(max_digits=12,decimal_places=2)
    slug = models.SlugField()
    image = models.ImageField(upload_to='products/images/',blank=True,null = True) # wiil be uploaded to MEDIA_ROOT/myFiles
    thumbnail = models.ImageField(upload_to = 'products/thumnails/', blank=True,null = True)
    is_published = models.BooleanField(default=True)
    comment = models.TextField('comments', blank=True,null=True)
    created_by = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    last_updated_by = models.OneToOneField(User,related_name = "product_created_by", null=True, on_delete=models.SET_NULL)
    date_last_updated = models.DateTimeField(auto_now_add=True,null=True)

    def get_inward_stock_total(self):
        # itms = StockItem.objects.filter(item = self.id)
        itms = self.stock_items.all()
        total = 0
        for i in itms:
            if(i.inward_stock is not None):
                sub_total = i.quantity * i.price
                total = total + sub_total

        return total
    
    def get_outward_stock_total(self):
        # itms = StockItem.objects.filter(item = self.id)
        itms = self.stock_items.all()
        total = 0
        for i in itms:
            if(i.outward_stock is not None):
                sub_total = i.quantity * i.price
                total = total + sub_total

        return total

    
    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return '%s [%s]' % (self.category, self.name)
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        else:
            return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300,200)):
        img = Image.open(image)
        img.convert('RGB') # MAkes The Image Transparent
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'PNG', quality=85)
        # transparent image can’t be stored into jpg or jpeg format
        # Can only be stored in PNG format 

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
    
class Service(models.Model):
    service_code = models.CharField(max_length=200,unique=True)
    name = models.CharField(unique=True, max_length=60,help_text="Name Of the Service")
    description = models.TextField(null=True,blank=True,help_text="Short Description Of the Service")
    created_by = models.OneToOneField(User,related_name = "service_created_by", null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    last_updated_by = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    date_last_updated = models.DateTimeField(auto_now_add=True,null=True)


class Supplier(models.Model):
    ENTITYTYPES = [
        ('INDIVIDUAL','INDIVIDUAL'),
        ('COMPANY', 'COMPANY'),
    ]
    name = models.CharField(unique=True,max_length=100)
    location = models.CharField(max_length=100)
    telephone = models.CharField(blank=True,null=True, max_length=100)
    entity_type = models.CharField(choices=ENTITYTYPES,blank=True,null=True,max_length=100)

class Consumer(models.Model):
    name = models.CharField(unique=True,max_length=100)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

@receiver(pre_save, sender = Category)
def unique_uc_code_generator(instance,new_code=None, *args,**kwargs):
    if(new_code is not None):
        code = new_code;
    else:
        code = "UC-10000"

    qs_exists = Category.objects.filter(cat_code= code).exists()
    if(qs_exists):
        new_code = "UC-{randstr}".format(
            randstr=random_string_generator(size=5)
        )
        return unique_uc_code_generator(instance,new_code=new_code,*args,**kwargs)
    instance.cat_code = code
    return code

@receiver(pre_save, sender = Item)
def unique_u_code_generator(instance,new_code=None, *args,**kwargs):
    if(new_code is not None):
        code = new_code;
    else:
        code = "U-10000"

    qs_exists = Item.objects.filter(item_code= code).exists()
    if(qs_exists):
        new_code = "U-{randstr}".format(
            randstr=random_string_generator(size=5)
        )
        return unique_u_code_generator(instance,new_code=new_code,*args,**kwargs)
    instance.item_code = code
    return code

@receiver(pre_save, sender = Service)
def unique_s_code_generator(instance,new_code=None, *args,**kwargs):
    if(new_code is not None):
        code = new_code;
    else:
        code = "U-10000"

    qs_exists = Service.objects.filter(service_code= code).exists()
    if(qs_exists):
        new_code = "U-{randstr}".format(
            randstr=random_string_generator(size=5)
        )
        return unique_s_code_generator(instance,new_code=new_code,*args,**kwargs)
    instance.service_code = code
    return code

@receiver(pre_save, sender = Item)
def unique_slug_generator(instance,new_slug=None, *args,**kwargs):
    if(new_slug is not None):
        slug = new_slug;
    else:
        slug = slugify(instance.name)

    qs_exists = Item.objects.filter(slug= slug).exists()
    if(qs_exists):
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance,new_slug=new_slug,*args,**kwargs)
    instance.slug = slug
    return slug