from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish')  # unique_for_date: один пост со слагом на заданную дату
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cd_posts')
    body = models.TextField()
    image = models.ImageField(upload_to='images/%Y/%m/%d', default=True, null=False, blank=False)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)  # дата будет сохраняться автоматически во время создания объекта
    updated = models.DateTimeField(auto_now=True)  # дата будет обновляться автоматически во время сохранения объекта
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT)
    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер
    tags = TaggableManager()  # менеджер tags позволит добавлять, извлекать и удалять теги из объектов Post.

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cd:post_detail', args=[self.publish.year,
                                               self.publish.month,
                                               self.publish.day,
                                               self.slug])


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )  # связывает каждый ком. с одним постом. Указанная взаимосвязь многие-к-одному определена в модели Comment
    name = models.CharField(max_length=40)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)  # по умолчанию все комментарии активны

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
