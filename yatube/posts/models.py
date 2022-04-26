from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Post(models.Model):
    text = models.TextField('Текст поста',
                            help_text='Введите текст поста'
                            )
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True
                                    )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='author',
                               verbose_name='Автор'
                               )
    group = models.ForeignKey('Group',
                              on_delete=models.SET_NULL,
                              related_name='related_name_group',
                              blank=True,
                              null=True,
                              verbose_name='Группа',
                              help_text='Выберите группу'
                              )
    image = models.ImageField('Картинка',
                              upload_to='posts/',
                              blank=True
                              )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text


class Group(models.Model):
    title = models.CharField('Title',
                             max_length=200
                             )
    slug = models.SlugField('Slug',
                            unique=True
                            )
    description = models.TextField('Description')

    class Meta:
        ordering = ('-title',)
        verbose_name = 'Группы'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post',
                             on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Коментарий к посту'
                             )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор'
                               )
    text = models.TextField('Текст Комментария',
                            help_text='Введите текст Комментария'
                            )
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True
                                    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following',
                               )

    class Meta:
        ordering = ('-user',)
        verbose_name = 'Подпись на автора'
        verbose_name_plural = 'Подпись на автора'
        unique_together = ('user', 'author')
        UniqueConstraint(fields=['user', 'author'],
                         name='unique_author_user')

    def __str__(self):
        return self.user
