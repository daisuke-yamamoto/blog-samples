# coding: utf-8
import json
from django.test import TestCase
from django.test.client import Client
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from sample1.mixins import LoginRequiredMixin, SuRequiredMixin


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

    def get(self, *args, **kwds):
        return self.request(*args, **kwds)

    def post(self, *args, **kwds):
        return self.request(is_post=True, *args, **kwds)

    def request(self, path, is_post=False, is_ajax=False, *args, **kwds):
        if is_ajax:
            kwds['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        if is_post:
            return self.client.post(path, *args, **kwds)
        else:
            return self.client.get(path, *args, **kwds)


class TestLoginRequiredMixin(TestViewBase):
    # テスト対象のmixinを設定します。
    _mixin = LoginRequiredMixin

    def setUp(self):
        super().setUp()
        self.path = reverse('test_sample1_loginrequiredmixin')

    def test_logged_in(self):
        """ログイン済みのテストです。"""
        # ユーザを作成し、ログインします。
        username = 'foo'
        password = 'secret'
        User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)

        # テスト対象を実行します。
        res = self.get(self.path)

        # テスト結果を確認します。
        self.assertEqual(res.status_code, 200)

    def test_not_logged_in(self):
        """ログインしていない場合のテストです。"""
        # テスト対象を実行します。
        res = self.get(self.path)

        # テスト結果を確認します。
        self.assertRedirects(res, settings.LOGIN_URL)

    def test_not_active(self):
        """ユーザがアクティブでない場合のテストです。"""
        username = 'foo'
        password = 'secret'
        user = User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)
        user.is_active = False
        user.save()

        # テスト対象を実行します。
        res = self.get(self.path)

        # テスト結果を確認します。
        self.assertEqual(res.status_code, 302)

    def test_not_logged_in_ajax(self):
        """ログインしていない場合のテストです。（ajax）"""
        # テスト対象を実行します。
        res = self.get(self.path, is_ajax=True)

        # テスト結果を確認します。
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.content.decode())
        self.assertTrue(data['login_required'])

    def test_not_active_ajax(self):
        """ユーザがアクティブでない場合のテストです。（ajax）"""
        username = 'foo'
        password = 'secret'
        user = User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)
        user.is_active = False
        user.save()

        # テスト対象を実行します。
        res = self.get(self.path, is_ajax=True)

        # テスト結果を確認します。
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.content.decode())
        self.assertTrue(data['login_required'])


class TestSuRequiredMixin(TestViewBase):
    # テスト対象のmixinを設定します。
    _mixin = SuRequiredMixin

    def setUp(self):
        super().setUp()
        self.path = reverse('test_sample1_surequiredmixin')

    def test_su_logged_in(self):
        """スーパーユーザでログイン済みのテストです。"""
        # スーパーユーザを作成し、ログインします。
        username = 'foo'
        password = 'secret'
        User.objects.create_superuser(
            username=username, password=password, email='dummy')
        self.client.login(username=username, password=password)

        # テスト対象を実行します。
        res = self.get(self.path)

        # テスト結果を確認します。
        self.assertEqual(res.status_code, 200)

    def test_logged_in(self):
        """ログイン済みのテストです。"""
        # ユーザを作成し、ログインします。
        username = 'foo'
        password = 'secret'
        User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)

        # テスト対象を実行します。
        res = self.get(self.path)

        # テスト結果を確認します。
        self.assertRedirects(res, reverse('member_home'))

    def test_not_logged_in(self):
        """ログインしていない場合のテストです。"""
        # テスト対象を実行します。
        res = self.get(self.path)

        # テスト結果を確認します。
        self.assertRedirects(res, settings.LOGIN_URL)

    def test_logged_in_ajax(self):
        """ログイン済みのテストです。（ajax）"""
        # ユーザを作成し、ログインします。
        username = 'foo'
        password = 'secret'
        User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)

        # テスト対象を実行します。
        res = self.get(self.path, is_ajax=True)

        # テスト結果を確認します。
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.content.decode())
        self.assertTrue(data['su_required'])

    def test_not_logged_in_ajax(self):
        """ログインしていない場合のテストです。（ajax）"""
        # テスト対象を実行します。
        res = self.get(self.path, is_ajax=True)

        # テスト結果を確認します。
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.content.decode())
        self.assertTrue(data['login_required'])
