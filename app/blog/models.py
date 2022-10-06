from django.db import models
from pytils.translit import slugify

from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(upload_to='media/', verbose_name='Изображение', )
    title = models.CharField(max_length=500, verbose_name='Заголовок поста', )
    content = RichTextUploadingField(verbose_name='Содержимое поста', )
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    slug = models.SlugField(max_length=200, unique=True, null=False, blank=False, default=slugify(title), verbose_name='Ссылка')

    class Meta:
        verbose_name = 'Пост на сайте'
        verbose_name_plural = 'Посты на сайте'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self, **kwargs):
        return f'/post/{self.slug}'


class Galery(models.Model):
    image = models.ImageField(upload_to='galery', verbose_name='Изображение', )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', default=None)
