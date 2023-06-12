from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.simple_tag
def total_posts():  # Django будет использовать имя функции в качестве имени тега.
    return Post.published.count()


@register.inclusion_tag(
    'cd/post/latest_posts.html')  # указан шаблон, который будет прорисовываться возвращенными значениями
def show_latest_posts(count=5):
    """Шаблонный тег будет принимать опциональный параметр count параметр позволит задавать число отображаемых постов"""
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


"""Теги включения должны возвращать словарь значений, который используется в качестве контекста для прорисовки заданного
 шаблона. Только созданный шаблонный тег позволяет задавать опциональное число отображаемых постов как 
 {% show_latest_posts 3 %}."""


@register.simple_tag
def get_most_commented_posts(count=5):
    """в шаблонном теге с помощью функции annotate() формируется набор запросов QuerySet, чтобы агрегировать общее число
        комментариев к каждому посту."""
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))