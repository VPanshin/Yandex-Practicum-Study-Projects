import shutil
import tempfile

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Comment, Follow, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test')
        cls.author = User.objects.create_user(username='author')
        cls.small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )
        cls.uploaded = SimpleUploadedFile(
            name="small.gif",
            content=cls.small_gif,
            content_type="image/gif"
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовый пост',
            group=cls.group,
            image=cls.uploaded,
        )
        cls.reverse_index = reverse('posts:index')
        cls.reverse_create = reverse('posts:post_create')
        cls.reverse_follow = reverse('posts:follow_index')
        cls.reverse_group = reverse(
            'posts:group_list', kwargs={'slug': cls.group.slug}
        )
        cls.reverse_profile = reverse(
            'posts:profile', kwargs={'username': cls.author}
        )
        cls.reverse_detail = reverse(
            'posts:post_detail', kwargs={'post_id': cls.post.id}
        )
        cls.reverse_edit = reverse(
            'posts:post_edit', kwargs={'post_id': cls.post.id}
        )
        cls.reverse_comment = reverse(
            "posts:add_comment", kwargs={"post_id": cls.post.id}
        )
        cls.templates_page_names_private = {
            cls.reverse_follow: 'posts/follow.html',
            cls.reverse_edit: 'posts/create_post.html',
            cls.reverse_create: 'posts/create_post.html',
        }
        cls.templates_page_names_public = {
            cls.reverse_index: 'posts/index.html',
            cls.reverse_group: 'posts/group_list.html',
            cls.reverse_profile: 'posts/profile.html',
            cls.reverse_detail: 'posts/post_detail.html',
        }
        cls.templates_page_names = {
            **cls.templates_page_names_private,
            **cls.templates_page_names_public,
        }

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        cache.clear()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(self.author)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for reverse_name, template in self.templates_page_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.author_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_pages_show_correct_context(self):
        """Список постов в шаблонах и шаблоны сформированы
        с правильным контекстом.
        """
        for reverse_name in self.templates_page_names_public:
            with self.subTest(reverse_name):
                response = self.guest_client.get(reverse_name)
                expected = list(
                    Post.objects.filter(text=self.post)[:settings.POST_LOAD]
                )
                if ["page_obj"] in expected:
                    self.assertEqual(
                        list(response.context["page_obj"]), expected
                    )
                elif ["post"] in expected:
                    self.assertEqual(
                        response.context["post"].text, self.post.text
                    )
                    self.assertEqual(
                        response.context["post"].author, self.post.author
                    )
                    self.assertEqual(
                        response.context["post"].group, self.post.group
                    )

    def test_create_show_correct_context(self):
        """Шаблон create_post и create_post(edit) сформирован
        с ожидаемым контекстом.
        """
        response = self.authorized_client.get(
            self.reverse_create
        )
        response = self.author_client.get(
            self.reverse_edit
        )
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context["form"].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_create_post_in_pages(self):
        """Проверяем создание поста на страницах с выбранной группой."""
        form_fields = {
            self.reverse_index: Post.objects.get(group=self.post.group),
            self.reverse_group: Post.objects.get(group=self.post.group),
            self.reverse_profile: Post.objects.get(group=self.post.group),
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                response = self.authorized_client.get(value)
                form_field = response.context["page_obj"]
                self.assertIn(expected, form_field)

    def test_check_group_not_in_mistake_group_list_page(self):
        """Проверяем чтобы созданный пост с группой не попап в чужую группу."""
        form_fields = {
            self.reverse_group: Post.objects.exclude(group=self.post.group),
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                response = self.authorized_client.get(value)
                form_field = response.context["page_obj"]
                self.assertNotIn(expected, form_field)

    def test_comment_correct_context(self):
        """Валидная форма Комментария создает запись в Post."""
        comments_count = Comment.objects.count()
        form_data = {"text": "Тестовый коммент"}
        response = self.authorized_client.post(
            self.reverse_comment,
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            self.reverse_detail,
        )
        self.assertEqual(Comment.objects.count(), comments_count + 1)
        self.assertTrue(
            Comment.objects.filter(text="Тестовый коммент").exists()
        )

    def test_image_in_pages(self):
        """Картинка передается на публичные страницы."""
        for url in self.templates_page_names_public:
            with self.subTest(url):
                response = self.guest_client.get(url)
                expected = Post.objects.filter(image=self.post.image)
                if ["page_obj"] in expected:
                    self.assertEqual(
                        response.context["page_obj"].image,
                        expected
                    )
                elif ["post"] in expected:
                    self.assertEqual(
                        response.context["post"].image,
                        expected
                    )

    def test_image_in_page(self):
        """Проверяем что пост с картинкой создается в БД."""
        self.assertTrue(
            Post.objects.filter(
                text=self.post.text, image=self.post.image
            ).exists()
        )

    def test_check_cache(self):
        """Проверка кеша."""
        response = self.guest_client.get(self.reverse_index)
        response_before = response.content
        Post.objects.latest().delete()
        response2 = self.guest_client.get(self.reverse_index)
        response_after = response2.content
        self.assertEqual(response_before, response_after)

    def test_follow_page(self):
        "Проверка системы подписки."
        # Проверяем, что страница подписок пуста
        response = self.authorized_client.get(self.reverse_follow)
        self.assertEqual(len(response.context["page_obj"]), 0)

        # Проверка подписки на автора поста
        Follow.objects.get_or_create(user=self.user, author=self.post.author)
        response2 = self.authorized_client.get(self.reverse_follow)
        self.assertEqual(len(response2.context["page_obj"]), 1)

        # Проверка подписки у юзера-фоловера
        self.assertIn(self.post, response2.context["page_obj"])

        # Проверка что пост не появился в избранных у юзера-обычного
        user = User.objects.create(username="TestUser")
        self.authorized_client.force_login(user)
        response2 = self.authorized_client.get(self.reverse_follow)
        self.assertNotIn(self.post, response2.context["page_obj"])

        # Проверка отписки от автора поста
        Follow.objects.all().delete()
        response3 = self.authorized_client.get(self.reverse_follow)
        self.assertEqual(len(response3.context["page_obj"]), 0)
