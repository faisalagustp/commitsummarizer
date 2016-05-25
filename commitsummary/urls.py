"""commitsummary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))

Alurnya:
Di Home Page, ada dua opsi:
* memunculkan semua repository yang telah tersimpan
* form untuk ngecrawl repository baru
* Ketika klik link, muncul link commit dan listnya (dan summarize bentuk popup)
* ketika klik commit, munculkan semua file yang dimodifikasi dan summarizenya
"""
from django.conf.urls import include, url
from django.contrib import admin
from cosum.views import views as cosum_views

urlpatterns = [
    url(r'^$', cosum_views.home_page, name="home"),
    url(r'^import/$', cosum_views.import_page, name="import"),
    url(r'^commit/$', cosum_views.commit_page, name="commit"),
    url(r'^detail/(\d+)/$', cosum_views.detail_page, name="detail"),
]
