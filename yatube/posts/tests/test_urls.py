from django.conf import settings
from django.test import Client, TestCase

from ..models import Group, Post, User


class StaticURLHomepageTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, settings.OK)

    def test_techpage(self):
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, settings.OK)

    def test_authorpage(self):
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, settings.OK)


class PostURLTests(TestCase):

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
        self.GROUP_SLUK = self.group.slug
        self.POST_PK = self.group.pk
        self.AUTHOR = self.user

    def test_urls_guest_client_correct_answer(self):
        """URL-адрес не авторизированый клиент."""
        urls_group = str(f'/group/{self.GROUP_SLUK}/')
        urls_edit = str(f'/posts/{self.POST_PK}/edit/')
        urls_add_com = str(f'/posts/{self.POST_PK}/comment/')
        data_check = {
            '/': settings.OK,
            '/about/tech/': settings.OK,
            '/about/author/': settings.OK,
            urls_group: settings.OK,
            urls_edit: settings.FOUND,
            '/create/': settings.FOUND,
            '/fdshfgd/': settings.NOT_FOUND,
            urls_add_com: settings.FOUND,
        }
        for adress, answer in data_check.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, answer)

    def test_urls_auth_client_correct_answer(self):
        """URL-адрес авторизированый клиент."""
        urls_group = str(f'/group/{self.GROUP_SLUK}/')
        urls_edit = str(f'/posts/{self.POST_PK}/edit/')
        urls_add_com = str(f'/posts/{self.POST_PK}/comment/')
        data_check = {
            '/': settings.OK,
            '/about/tech/': settings.OK,
            '/about/author/': settings.OK,
            urls_group: settings.OK,
            urls_edit: settings.OK,
            '/create/': settings.OK,
            '/fdshfgd/': settings.NOT_FOUND,
            urls_add_com: settings.FOUND,
        }
        for adress, answer in data_check.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertEqual(response.status_code, answer)

    def test_urls_user_template(self):
        """URL-адрес использует соответствующий шаблон."""
        urls_group = str(f'/group/{self.GROUP_SLUK}/')
        urls_auth = str(f'/profile/{self.AUTHOR}/')
        urls_post_edit = str(f'/posts/{self.POST_PK}/edit/')
        templates_url_names = {
            '/': 'posts/index.html',
            '/create/': 'posts/create.html',
            urls_group: 'posts/group_list.html',
            urls_auth: 'posts/profile.html',
            urls_post_edit: 'posts/create.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
