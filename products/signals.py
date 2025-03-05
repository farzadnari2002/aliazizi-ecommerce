from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import FavoriteProduct, CommentProduct


# Favorites Logic
@receiver(post_save, sender=FavoriteProduct)
def increment_favorites_count(sender, instance, **kwargs):
    instance.product.favorites_count += 1
    instance.product.save()

@receiver(post_delete, sender=FavoriteProduct)
def decrement_favorites_count(sender, instance, **kwargs):
    instance.product.favorites_count -= 1
    instance.product.save()


# Comments Logic
@receiver(post_save, sender=CommentProduct)
def increment_comment_count(sender, instance, **kwargs):
    instance.product.comments_count += 1
    instance.product.save()

@receiver(post_delete, sender=CommentProduct)
def decrement_comment_count(sender, instance, **kwargs):
    instance.product.comments_count -= 1
    instance.product.save()



