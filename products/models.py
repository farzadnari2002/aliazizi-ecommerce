from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from accounts.models import User
from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey
from autoslug import AutoSlugField
from colorfield.fields import ColorField
import uuid
from utils.validators import validate_image_dimensions, validate_image_size
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class CategoryProduct(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']
    
    def __str__(self):
        return self.name


class ColorProduct(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color_code = ColorField()

    def __str__(self):
        return self.name


class SizeProduct(models.Model):
    size = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.size


def get_upload_to(instance, filename):
        return f'products/{instance}/{filename}'


class ImagesProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_upload_to)

    def __str__(self):
        return f'image: {self.product}'


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True, editable=False)
    tags = TaggableManager()
    sku = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=get_upload_to, validators=[validate_image_size, validate_image_dimensions])
    image_thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFill(100, 100)],
                                      format='JPEG',
                                      options={'quality': 60})
    short_desc = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, related_name='products')
    color = models.ManyToManyField(ColorProduct, related_name='products')
    size = models.ManyToManyField(SizeProduct, related_name='products')
    is_published = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def avg_rating(self):
        return self.comments.aggregate(models.Avg('rating'))['rating__avg']


class SpecificationsProduct(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField(validators=[MaxLengthValidator(300)])
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='specifications')

    def __str__(self):
        return self.title


class CommentProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(validators=[MinLengthValidator(1), MaxLengthValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f'comment: {self.user} - {self.product}'
