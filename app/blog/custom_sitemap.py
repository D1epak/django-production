"""
/**
 * Plugin Name:  custom-sitemap.xml
 * Template:    wp-reboot
 * Description: минималистичный блог для размещения ваших постов
 *
 * Theme URI:   https://github.com/KillNet73/wpreboot
 * Author:      KillNet73
 * Author URI:  https://github.com/KillNet73/
 *
 * Tags:        black, brown, orange, minimal
 * Text Domain: https://killnet73.ru
 *
 * License:     Лицензия. GNU General Public License v2 or later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 *
 * Version:     2.0
 */
"""

from django.core.paginator import Paginator
from django.shortcuts import render

from blog.models import Post


def custom_sitemap(request):
    """
    Плагин, который генерирует кастомный sitemap.xml с пагинацией
    на условии: 1000 постов на одну страницу, с элементами управления
    """
    contact_list = Post.objects.all()
    paginator = Paginator(contact_list, 5)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'theme/addon/custom_sitemap/sitemap.html', {'page_obj': page_obj})
