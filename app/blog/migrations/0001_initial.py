# Generated by Django 4.1 on 2022-09-10 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='Изображение')),
                ('title', models.CharField(blank=True, max_length=500, null=True, verbose_name='Заголовок поста')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Содержимое поста')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Пост на сайте',
                'verbose_name_plural': 'Посты на сайте',
                'ordering': ['-id'],
            },
        ),
    ]
