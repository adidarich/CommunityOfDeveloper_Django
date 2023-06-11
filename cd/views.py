from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST


def post_list(request):
    postlist = Post.published.all()

    # создаем экземпляр класса Paginator с числом объектов, возвращаемых в расчете на страницу
    paginator = Paginator(postlist, 5)

    # извлекаем HTTP GET-параметр page и сохраняем его в переменной page_number. Этот параметр содержит запрошенный
    # номер страницы. Если параметра page нет в GET-параметрах запроса, то мы используем стандартное значение 1,
    # чтобы загрузить первую страницу результатов.
    page_number = request.GET.get('page', 1)
    try:
        # получаем объекты для желаемой страницы, вызывая метод page() класса Paginator.
        # Этот метод возвращает объект Page, который хранится в переменной posts.
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    return render(request, 'cd/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # Список активных комментариев к этому посту
    comments = post.comments.filter(active=True)
    # Форма для комментирования пользователями
    form = CommentForm()

    return render(request, 'cd/post/detail.html', {'post': post, 'comments': comments, 'form': form})


def post_share(request, post_id):
    # Извлечь пост по идентификатору id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data  # Указанный атрибут представляет собой словарь полей формы и их значений
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'cd/post/share.html',
                  {'post': post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )  # по id поста извлекается опубликованный пост, используя функцию сокращенного доступа get_object_or_404
    comment = None  # хранения комментарного объекта при его создании
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)  # подход позволяет видоизменять объект перед его окончательным сохранением
        comment.post = post  # пост назначается созданному комментарию
        # Сохранить комментарий в базе данных
        comment.save()
    return render(request,
                  'cd/post/comment.html',
                  {'post': post, 'form': form, 'comment': comment})
