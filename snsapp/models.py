from django.db import models
from django.contrib.auth import get_user_model
from ecapp.models import Product


class Article(models.Model):
    """投稿記事"""
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    good_count = models.PositiveIntegerField(default=0)
    pub_date = models.DateTimeField(auto_now=True)


class Good(models.Model):
    """いいねカウント"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
