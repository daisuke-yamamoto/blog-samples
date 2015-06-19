# coding: utf-8
from django.conf.urls import patterns, url
from myapp.urls import urlpatterns
from sample1 import tests as sample1_tests

urlpatterns += patterns(
    '',
    url(r'^test/sample1/login_required_mixin1/$',
        sample1_tests.TestLoginRequiredView.as_view(),
        name='test_sample1_login_required_mixin1'),
    url(r'^test/sample1/login_required_mixin2/$',
        sample1_tests.TestLoginRequiredMixin2.as_view(),
        name='test_sample1_login_required_mixin2'),
    url(r'^test/sample1/login_required_mixin3/$',
        sample1_tests.TestLoginRequiredMixin3.as_view(),
        name='test_sample1_login_required_mixin3'),
)
