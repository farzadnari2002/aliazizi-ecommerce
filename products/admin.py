from django.contrib import admin
from . import models


admin.site.register(models.Product)
admin.site.register(models.CategoryProduct)
admin.site.register(models.ColorProduct)
admin.site.register(models.ImagesProduct)
admin.site.register(models.SpecificationsProduct)
admin.site.register(models.CommentProduct)
