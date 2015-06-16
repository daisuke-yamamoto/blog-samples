# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    """
    ログイン済みかをチェックするmixinです。
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwds):
        return super().dispatch(request, *args, **kwds)
