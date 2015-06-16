# coding: utf-8
from django.test import TestCase
from django.test.client import Client
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from sample1.mixins import LoginRequiredMixin


class TestLoginRequiredView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwds):
        return HttpResponse()

    def post(self, request, *args, **kwds):
        return HttpResponse()


class TestLoginRequiredMixin1(TestCase):
    # テスト用のURLパターンを使用します。
    urls = 'myapp.test_urls'

    def setUp(self):
        super().setUp()
        self.client = Client()
        # テスト用URL（test/sample1/login_required_mixin1/）を取得します。
        self.path = reverse('test_sample1_login_required_mixin1')

    def test_logged_in(self):
        """ログイン済みのテストです。"""
        # ユーザを作成し、ログインします。
        username = 'foo'
        password = 'secret'
        User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)

        # テスト対象を実行します。
        res = self.client.get(self.path)

        # テスト結果を確認します。
        self.assertEqual(res.status_code, 200)

    def test_not_logged_in(self):
        """ログインしていない場合のテストです。"""
        # テスト対象を実行します。
        res = self.client.get(self.path)

        # テスト結果を確認します。
        self.assertEqual(res.status_code, 302)


class TestLoginRequiredMixin2(TestCase):
    # テスト用のURLパターンを使用します。
    urls = 'myapp.test_urls'

    def setUp(self):
        super().setUp()
        self.client = Client()
        # テスト用URL（test/sample1/login_required_mixin2/）を取得します。
        self.path = reverse('test_sample1_login_required_mixin2')

    @classmethod
    def as_view(cls, **initkwds):
        cls = type('TestTempClass', (LoginRequiredMixin, View), {})
        cls.get = lambda self, request, *args, **kwargs: HttpResponse()
        cls.post = lambda self, request, *args, **kwargs: HttpResponse()
        return cls.as_view()

    def test_logged_in(self):
        """ログイン済みのテストです。"""
        # ユーザを作成し、ログインします。
        username = 'foo'
        password = 'secret'
        User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)

        # テスト対象を実行します。
        res = self.client.get(self.path)

        # テスト結果を確認します。
        self.assertEqual(res.status_code, 200)

    def test_not_logged_in(self):
        """ログインしていない場合のテストです。"""
        # テスト対象を実行します。
        res = self.client.get(self.path)

        # テスト結果を確認します。
        self.assertEqual(res.status_code, 302)


class TestViewBase(TestCase):
    urls = 'myapp.test_urls'
    _mixin = None

    def setUp(self):
        super().setUp()
        self.client = Client()

    @classmethod
    def as_view(cls, **initkwds):
        cls = type('TestTempClass', (cls._mixin, View), {})
        cls.get = lambda self, request, *args, **kwargs: HttpResponse()
        cls.post = lambda self, request, *args, **kwargs: HttpResponse()
        return cls.as_view()


class TestLoginRequiredMixin3(TestViewBase):
    # テスト対象のmixinを設定します。
    _mixin = LoginRequiredMixin

    def setUp(self):
        super().setUp()
        # テスト用URL（test/sample1/login_required_mixin3/）を取得します。
        self.path = reverse('test_sample1_login_required_mixin3')

    def test_logged_in(self):
        """ログイン済みのテストです。"""
        # ユーザを作成し、ログインします。
        username = 'foo'
        password = 'secret'
        User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)

        # テスト対象を実行します。
        res = self.client.get(self.path)

        # テスト結果を確認します。
        self.assertEqual(res.status_code, 200)

    def test_not_logged_in(self):
        """ログインしていない場合のテストです。"""
        # テスト対象を実行します。
        res = self.client.get(self.path)

        # テスト結果を確認します。
        self.assertEqual(res.status_code, 302)
