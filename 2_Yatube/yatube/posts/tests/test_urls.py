from http import HTTPStatus

from django.test import Client, TestCase

from ..models import Group, Post, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test')
        cls.author = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовый пост',
            group=cls.group,
        )
        cls.templates_url_names_public = {
            "/": "posts/index.html",
            f"/group/{cls.group.slug}/": "posts/group_list.html",
            f"/profile/{cls.user.username}/": "posts/profile.html",
            f"/posts/{cls.post.id}/": "posts/post_detail.html",
        }
        cls.templates_url_names_private = {
            "/follow/": "posts/follow.html",
            "/create/": "posts/create_post.html",
            f"/posts/{cls.post.id}/edit/": "posts/create_post.html",
        }
        cls.templates_url_names = {
            **cls.templates_url_names_public,
            **cls.templates_url_names_private,
        }
        cls.redirect_public = {
            "/create/": "/auth/login/?next=/create/",
            f"/posts/{cls.post.id}/edit/":
            (f'/auth/login/?next=/posts/{cls.post.id}/edit/'),
            f"/profile/{cls.user.username}/follow/":
            (f'/auth/login/?next=/profile/{cls.user.username}/follow/'),
        }
        cls.redirect_private = {
            f"/posts/{cls.post.id}/comment/": f"/posts/{cls.post.id}/",
            f"/profile/{cls.user.username}/follow/": "/follow/",
            f"/profile/{cls.user.username}/unfollow/": "/follow/",
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(self.author)

    def test_public_urls_exists_at_desired_location(self):
        """URL-адреса доступны любому пользователю."""
        for url in self.templates_url_names_public:
            with self.subTest(url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_private_urls_exists_at_desired_location(self):
        """URL-адреса доступны любому автору."""
        for url in self.templates_url_names_private:
            with self.subTest(url):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for url, template in self.templates_url_names.items():
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_urls_redirect_anonymous_on_auth_login(self):
        """Страницы перенаправят анонимного пользователя
        на страницу логина.
        """
        for url, redirect in self.redirect_public.items():
            with self.subTest(url):
                response = self.guest_client.get(url)
                self.assertRedirects(response, redirect)

    def test_post_unexisting_page_at_desired_location(self):
        """Страница /unexisting_page/ должна выдавать ошибку о
        несуществующей странице.
        """
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_redirect_user_on_post_or_follow(self):
        """Страницы перенаправят пользователя
        на страницу поста или подписки.
        """
        for url, redirect in self.redirect_private.items():
            with self.subTest(url):
                response = self.authorized_client.get(url)
                self.assertRedirects(response, redirect)
