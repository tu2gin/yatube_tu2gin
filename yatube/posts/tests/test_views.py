from django import forms
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import ImageFieldFile
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Comment, Group, Post, User


class PostViewsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая группа',
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        Post.objects.create(
            author=self.user,
            text='Тестовая группа',)
        self.GROUP_SLUK = self.group.slug
        self.POST_PK = self.group.pk
        self.AUTHOR = self.user

    def test_index_page_uses_correct_template(self):
        """URL-адрес использует шаблон posts/index.html."""
        response = self.authorized_client.get(reverse(
            'posts:index'))
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_group_posts_views_correct_template(self):
        """URL-адрес использует шаблон posts/group_list.html."""
        response = self.authorized_client.get(reverse(
            'posts:group_posts', kwargs={'slug': self.GROUP_SLUK}))
        self.assertTemplateUsed(response, 'posts/group_list.html')

    def test_create_page_views_correct_template(self):
        """URL-адрес использует шаблон posts/create.html."""
        response = self.authorized_client.get(reverse(
            'posts:create'))
        self.assertTemplateUsed(response, 'posts/create.html')

    def test_post_edit_page_views_correct_template(self):
        """URL-адрес использует шаблон для post_edit."""
        response = self.authorized_client.get(reverse(
            'posts:post_edit', args=[self.POST_PK]))
        self.assertTemplateUsed(response, 'posts/create.html')

    def test_profile_page_uses_correct_template(self):
        """URL-адрес использует шаблон profile.html."""
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': self.AUTHOR}))
        self.assertTemplateUsed(response, 'posts/profile.html')

    def test_post_detail_page_uses_correct_template(self):
        """URL-адрес использует шаблон posts_detail.html."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.POST_PK}))
        self.assertTemplateUsed(response, 'posts/post_detail.html')


class PostContextImg(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='text',
            slug='test-slug',
            description='text',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='text',
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        small_gif = (b'\x47\x49\x46\x38\x39\x61\x02\x00'
                     b'\x01\x00\x80\x00\x00\x00\x00\x00'
                     b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                     b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                     b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                     b'\x0A\x00\x3B'
                     )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        self.img_name = uploaded.name
        for i in range(10):
            Post.objects.create(
                author=self.user,
                text='text',
                group=self.group,
                image=uploaded)

    def test_index_img(self):
        """Шаблон index с правильным контекстом И имеет картинку."""
        response = self.guest_client.get(reverse(
            'posts:index'))
        first_object = response.context['page_obj'][0]
        image_Field = first_object.image
        self.assertIsInstance(image_Field, ImageFieldFile)


class PostContextTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='text',
            slug='test-slug',
            description='text',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='text',
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        small_gif = (b'\x47\x49\x46\x38\x39\x61\x02\x00'
                     b'\x01\x00\x80\x00\x00\x00\x00\x00'
                     b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                     b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                     b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                     b'\x0A\x00\x3B'
                     )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        self.img_name = uploaded.name
        for i in range(10):
            Post.objects.create(
                author=self.user,
                text='text',
                group=self.group,
                image=uploaded)

    def test_index_page_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:index'))
        first_object = response.context['page_obj'][0]
        index_posts_text = first_object.text
        self.assertEqual(index_posts_text, 'text')

    def test_group_posts_page_correct_context(self):
        """Шаблон group_posts сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:group_posts', kwargs={'slug': self.group.slug}))
        first_object = response.context['page_obj'][0]
        group_posts_title = response.context['title']
        group_posts_text = first_object.text
        group_posts_slug = first_object.group.slug
        self.assertEqual(group_posts_title, 'text')
        self.assertEqual(group_posts_text, 'text')
        self.assertEqual(group_posts_slug, 'test-slug')

    def test_profile_page_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': self.user.username}))
        first_object = response.context['page_obj'][0]
        profile_posts_text = first_object.text
        profile_author = response.context['author'].username
        self.assertEqual(profile_posts_text, 'text')
        self.assertEqual(profile_author, self.user.username)

    def test_post_detail_page_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': self.post.pk}))
        post_text = response.context['post']
        self.assertEqual(post_text.text, 'text')

    def test_posts_create_page_show_form_correct_context(self):
        """Шаблон create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_posts_edit_page_show_form_correct_context(self):
        """Шаблон edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': self.post.pk}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='text',
            slug='test-slug',
            description='text',
        )

    def setUp(self):
        self.guest_client = Client()
        for i in range(13):
            Post.objects.create(
                author=self.user,
                text=str(f'text {i}'),
                group=self.group)

    def test_index_first_page_contains_ten_records(self):
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), settings.PAG_POST)

    def test_index_second_page_contains_three_records(self):
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_group_list_first_page_contains_ten_records(self):
        response = self.client.get(reverse(
            'posts:group_posts', kwargs={'slug': self.group.slug}))
        self.assertEqual(len(response.context['page_obj']), settings.PAG_POST)

    def test_group_list_second_page_contains_three_records(self):
        response = self.client.get(reverse(
            'posts:group_posts',
            kwargs={'slug': self.group.slug}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_profile_first_page_contains_ten_records(self):
        response = self.client.get(reverse(
            'posts:profile', kwargs={'username': self.user.username}))
        self.assertEqual(len(response.context['page_obj']), settings.PAG_POST)

    def test_profile_second_page_contains_three_records(self):
        response = self.client.get(reverse(
            'posts:profile',
            kwargs={'username': self.user.username}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)


class PostAddTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая группа',
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        for i in range(10):
            Post.objects.create(
                author=self.user,
                text='text',
                group=self.group)

    def test_add_post(self):
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)
        posts_count_index = Post.objects.count()
        posts_count_profile = Post.objects.filter(author=self.user).count()
        posts_count_group = Post.objects.filter(group=self.group.pk).count()
        small_gif = (b'\x47\x49\x46\x38\x39\x61\x02\x00'
                     b'\x01\x00\x80\x00\x00\x00\x00\x00'
                     b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                     b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                     b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                     b'\x0A\x00\x3B'
                     )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        Post.objects.create(
            author=self.user,
            text='text',
            group=self.group,
            image=uploaded)
        posts_add_index = Post.objects.count()
        posts_add_profile = Post.objects.filter(author=self.user).count()
        posts_add_group = Post.objects.filter(group=self.group.pk).count()
        self.assertEqual(posts_count_index + 1, posts_add_index)
        self.assertEqual(posts_count_profile + 1, posts_add_profile)
        self.assertEqual(posts_count_group + 1, posts_add_group)


class CommentAddTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая группа',
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        for i in range(10):
            Post.objects.create(
                author=self.user,
                text='text',
                group=self.group)

    def test_add_comment(self):
        comment_count = Comment.objects.filter(post=self.post).count()
        Comment.objects.create(
            author=self.user,
            text='text',
            post=self.post)
        comment_count_add = Comment.objects.filter(post=self.post).count()
        self.assertEqual(comment_count + 1, comment_count_add)


class TestCache(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая группа',
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        for i in range(1):
            Post.objects.create(
                author=self.user,
                text='text',
                group=self.group)

    def test_index_cache(self):
        expected_post = Post.objects.latest('pub_date')
        response = self.client.get(reverse('posts:index'))
        post = response.content
        print(expected_post)
        Post.objects.latest('pub_date').delete()
        response = self.client.get(reverse('posts:index'))
        post = response.content
        self.assertNotEqual(post, expected_post)
