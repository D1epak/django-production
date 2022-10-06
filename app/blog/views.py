from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from django.core.files.base import File
from django.core.files.temp import NamedTemporaryFile
from django.views.generic import ListView, TemplateView
from pytils.translit import slugify
from randomfilestorage.storage import RandomFileSystemStorage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from blog.models import Post, Galery

import requests
import re


class Index(TemplateView):
    """
    Класс отображения главной страницы
    использует методы контекстной обработки модели
    """
    template_name = 'theme/page/index.html'

    def get_context_data(self, **kwargs):
        slider = Post.objects.order_by('-date').order_by("?")[0:4]
        post = Post.objects.order_by('-date')[0:6]

        context = {
            'slider': slider,
            'post': post
        }
        return context


class PostDetail(TemplateView):
    """
    Класс отображения страницы детального просмотра поста
    использует методы контекстной обработки модели
    """
    template_name = 'theme/page/detail.html'

    def get_context_data(self, **kwargs):
        post = Post.objects.get(slug=kwargs['slug'])
        share = Post.objects.order_by('-date').order_by("?")[0:8]
        share_left = Post.objects.order_by('-date').order_by("?")[0:5]
        context = {
            'post': post,
            'share': share,
            'share_left': share_left,
        }
        return context


class YandexTurbo(ListView):
    """
    Класс отображения страницы плагина yandex_turbo
    использует методы стандартный метод обработки модели
    и пагинацию на условии: 1000 постов на 1 странице
    """
    template_name = 'theme/addon/yandex_turbo/turbo.xml'
    model = Post
    context_object_name = 'turbo'
    paginate_by = 1000


# Объявление переменной для библиотеки django-random-filestorage
random_storage = RandomFileSystemStorage(location='/media/')


class ParceObjects(APIView):
    """
    Класс DRF создания поста в блог используя API
    """
    post_content = ""
    post_image_list = ""

    def change_content(self, galery: list, post):
        content = self.post_content
        for tag in range(0, len(content)):
            if 'img' in content[tag]:
                matches = len(re.findall(r'\ssrc="([^"]+)"', content[tag]))
                mapping = dict(zip(self.post_image_list[:matches], galery[:matches]))

                del self.post_image_list[:matches]
                del galery[:matches]

                for image_src, image_dst in mapping.items():
                    content[tag] = content[tag].replace(image_src, image_dst)

        content = "".join(content)

        Post.objects.filter(id=post.id).update(content=content)

    def save_images_to_galery(self, title, images: list, post):
        count = 0
        galery = []
        disable_warnings(InsecureRequestWarning)
        for image in images:  # получаю список с ссылками на фото
            count += 1
            img_temp = NamedTemporaryFile()
            req = requests.get(image, verify=False).content
            img_temp.write(req)
            img_temp.flush()
            photo = Galery.objects.create(image=File(img_temp, name=f'{title}-{count}.jpg'), post=post)
            galery.append(photo.image.url)

        self.change_content(galery, post)

    def post(self, request):
        try:
            form = request.data
            title = form['title']
            self.post_content = form['content']
            self.post_image_list = form['img_list']
            slug = slugify(title)
            amount_of_posts = Post.objects.all().count()
            slug = f'{slug}-{int(amount_of_posts) + 1}'
            img_temp = NamedTemporaryFile()
            req = requests.get(form['image'], verify=False).content
            img_temp.write(req)
            img_temp.flush()
            post = Post.objects.create(title=form['title'], content="".join(form['content']),
                                       image=File(img_temp, name=f'{title}.jpg'),
                                       slug=slug)

            self.save_images_to_galery(title, self.post_image_list, post)

            return Response('Post Created', status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
