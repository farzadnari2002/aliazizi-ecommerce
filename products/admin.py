from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from . import models


admin.site.register(models.Product)
admin.site.register(models.LikeProduct)
admin.site.register(models.ColorProduct)
admin.site.register(models.SizeProduct)
admin.site.register(models.ImagesProduct)
admin.site.register(models.SpecificationsProduct)
admin.site.register(models.CommentProduct)
admin.site.register(
    models.CategoryProduct,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
)
