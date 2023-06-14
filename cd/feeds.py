import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post


# новостная лента

class LatestPostsFeed(Feed):
    title = 'CD'
    link = reverse_lazy('cd:post_list')
    description = "New posts of CommunityOfDeveloper"

    def items(self):
        """items() извлекает включаемые в новостную ленту объекты, извлекаем последние пять опубликованных постов,
        которые затем будут включены в новостную ленту."""
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        """в методе item_description() используется функция markdown() , чтобы конвертировать контент в формате Markdown
         в формат HTML, и функция шаблонного фильтра truncatewords_html(), чтобы сокращать описание постов
         после 30 слов, избегая незакрытых HTML-тегов."""
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish


"""item_title(), item_description() и item_pubdate() будут получать каждый возвращаемый методом items() объект 
и возвращать заголовок, описание и дату публикации по каждому элементу."""
