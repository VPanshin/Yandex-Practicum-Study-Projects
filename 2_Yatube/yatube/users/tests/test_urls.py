from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test')
        cls.templates_any = [
            "/auth/signup/",
            "/auth/login/",
            "/auth/logout/",
            "/auth/reset/done/",
        ]
        cls.templates_user = [
            "/auth/password_reset/",
            "/auth/password_change/",
            "/auth/password_change/done/",
            "/auth/password_reset/done/",
        ]
        cls.templates_url_names = {
            "/auth/signup/": "users/signup.html",
            "/auth/login/": "users/login.html",
            "/auth/logout/": "users/logged_out.html",
            "/auth/reset/done/": "users/password_reset_complete.html",
            "/auth/password_reset/": "users/password_reset_form.html",
            "/auth/password_reset/done/": "users/password_reset_done.html",
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_any_exists_at_desired_location(self):
        """URL-адреса доступны любому пользователю."""
        for adress in self.templates_any:
            with self.subTest(adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_user_exists_at_desired_location(self):
        """URL-адреса доступны залогиненому пользователю."""
        for adress in self.templates_user:
            with self.subTest(adress):
                response = self.authorized_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for url, template in self.templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_change_url_redirect_anonymous_on_auth_login(self):
        """Страница /password_change/ перенаправит анонимного пользователя
        на страницу логина.
        """
        response = self.guest_client.get('/auth/password_change/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/auth/password_change/')

    def test_change_done_url_redirect_anonymous_on_auth_login(self):
        """Страница /password_change/done/ перенаправит анонимного пользователя
        на страницу логина.
        """
        response = self.guest_client.get(
            '/auth/password_change/done/', follow=True)
        self.assertRedirects(
            response, ('/auth/login/?next=/auth/password_change/done/'))
