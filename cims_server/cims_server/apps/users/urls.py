"""
URL configuration for cims_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

urlpatterns = [
    # 区块链对接测试
    # path('test/', views.TestView.as_view()),

    # 政府角色接口,无需登录
    # GET->获取所有普通用户的公钥 POST->创建普通用户
    path('users/', views.UsersView.as_view()),
    # GET->查询该普通用户的私钥
    path('users/<int:pk>/', views.UserDetailView.as_view()),
    # GET->获取所有拥有身份证/护照的普通用户
    path('users/certificate/', views.UserCertificatesView.as_view()),
    # GET->获取指定普通用户的所有身份证/护照
    path('users/certificate/<int:pk>/', views.UserSpecificCertificatesView.as_view()),
    # POST->为指定用户添加新的身份证
    path('users/id_card/<int:pk>/', views.AddIdentityCardView.as_view()),
    # POST->为指定用户添加新护照
    path('users/passport/<int:pk>/', views.AddPassportView.as_view()),

    # 普通用户角色接口,需要登录
    # GET->获取当前登录的普通用户的所有身份证/护照
    path('certificate/', views.CertificatesView.as_view()),
    # GET->获取当前用户最新的身份证/护照
    path('certificate/latest/', views.CertificatesLatestView.as_view()),

]
