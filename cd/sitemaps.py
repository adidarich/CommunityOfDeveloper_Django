from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    """Атрибуты changefreq и priority указывают частоту изменения страниц постов и
    их релевантность на веб-сайте (максимальное значение равно 1).
        changefreq и priority могут быть либо методами, либо атрибутами."""
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        """метод items() возвращает набор запросов QuerySet объектов, подлежащих включению в эту карту сайта
           по умолчанию Django вызывает метод get_absolute_url() по каждому объекту, чтобы получить его URL-адрес.
        """
        return Post.published.all()

    def lastmod(self, obj):
        """метод lastmod получает каждый возвращаемый методом items() объект и возвращает время последнего
        изменения объекта."""
        return obj.updated
