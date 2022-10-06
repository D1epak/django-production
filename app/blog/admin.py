from django.contrib import admin
from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django.utils.safestring import mark_safe

from . import models


class PostAdminForm(forms.ModelForm):
    """
    Инициализация модели базы данных для управления в админ панели
    """
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = models.Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    """
    Класс управления админ панелью и ее кастомизации
    Добавление элементов управления админ панелью
    Добавление миниатюр и slug поля при создании поста
    """
    form = PostAdminForm
    list_display = ('get_html_photo', 'title', 'date', 'slug')
    list_filter = ['date']
    search_fields = ['title']

    prepopulated_fields = {"slug": ("title",)}

    def get_html_photo(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50>")
        else:
            return "Нет фото"

    get_html_photo.short_description = "Миниатюра"


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Galery, )
