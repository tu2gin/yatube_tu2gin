from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.authorized_client = Client()
        cls.group = Group.objects.create(
            title='text',
            slug='test-slug',
            description='text',
        )
        for i in range(13):
            Post.objects.create(
                author=cls.user,
                text='text',
                group=cls.group)

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.GROUP_SLUK = self.group.slug
        self.POST_PK = self.group.pk
        self.AUTHOR = self.user

    def test_create_post(self):
        """Валидная форма создает запись в post."""
        posts_count = Post.objects.count()
        group_slug = self.group.pk
        form_data = {
            'text': 'test_text_add_post',
            'group': group_slug,
        }
        response = self.authorized_client.post(
            reverse('posts:create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.AUTHOR}))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        count_post_unique = Post.objects.filter(
            text='test_text_add_post', group=group_slug,).count()
        self.assertEqual(count_post_unique, 1)


class PostEditFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.authorized_client = Client()
        cls.group = Group.objects.create(
            title='text',
            slug='test-slug',
            description='text',
        )
        for i in range(13):
            Post.objects.create(
                author=cls.user,
                text='text',
                group=cls.group)

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_edit_post(self):
        """Валидная форма создает запись в post."""
        posts_count = Post.objects.count()
        post_edit = Post.objects.latest('pub_date')
        POST_PK = post_edit.pk
        group_slug = self.group.pk
        form_data = {
            'text': 'test_text_edit_post',
            'group': group_slug,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': POST_PK}),
            data=form_data,
            follow=True
        )
        post_last = Post.objects.latest('pub_date')
        LAST_PK = post_last.pk
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': LAST_PK}))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertEqual(post_last.text, 'test_text_edit_post')
