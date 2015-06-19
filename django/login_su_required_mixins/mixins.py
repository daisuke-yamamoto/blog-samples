# coding: utf-8
from functools import wraps
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def login_required(view):
    """
    ログイン済みかをチェックします。
    また、is_activeがTrueであることも確認します。
    """
    @wraps(view)
    def inner(request, *args, **kwds):
        if not request.user.is_authenticated() or not request.user.is_active:
            # ログインしていない、またはユーザが無効になっている場合
            if request.is_ajax():
                # ajaxの場合、403を返します。
                return JsonResponse({'login_required': True}, status=403)
            else:
                # ajaxではない場合、ログイン画面にリダイレクトします。
                return redirect(settings.LOGIN_URL)
        return view(request, *args, **kwds)
    return inner


def su_required(view):
    """
    ログイン済みで、かつスーパーユーザかをチェックするデコレータです。
    """
    @wraps(view)
    def inner(request, *args, **kwds):
        if not request.user.is_superuser:
            # スーパーユーザでない時は
            if request.is_ajax():
                # ajaxの場合、403を返します。
                return JsonResponse({'su_required': True}, status=403)
            else:
                # 「member_home」にリダイレクトします。
                return redirect(reverse('member_home'))
        return view(request, *args, **kwds)
    return inner


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwds):
        """ログイン済みかをチェックします。"""
        return login_required(super().as_view(**kwds))


class SuRequiredMixin(object):
    """
    管理者権限をチェックするMixinです。
    """
    @classmethod
    def as_view(cls, **kwds):
        """ログイン済みで、かつスーパーユーザかをチェックします。"""
        view = super().as_view(**kwds)
        # スーパーユーザのチェックよりも前に、
        # ログイン済みのチェックをするようにラップします。
        return login_required(su_required(view))
