"""LibraryDjangoApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

app_name = "main"

urlpatterns = [
    path('t/', views.BookListView.as_view(ordering=['TITLE']), name="homepage"),
    path('-t/', views.BookListView.as_view(ordering=['-TITLE']), name="homepage"),
    path('a/', views.BookListView.as_view(ordering=['AUTHOR']), name="homepage"),
    path('-a/', views.BookListView.as_view(ordering=['-AUTHOR']), name="homepage"),
    path('d/', views.BookListView.as_view(ordering=['DATE']), name="homepage"),
    path('-d/', views.BookListView.as_view(ordering=['-DATE']), name="homepage"),
    path('l/', views.BookListView.as_view(ordering=['LANGUAGE']), name="homepage"),
    path('-l/', views.BookListView.as_view(ordering=['-LANGUAGE']), name="homepage"),
    path('c/', views.BookListView.as_view(ordering=['CATEGORY']), name="homepage"),
    path('-c/', views.BookListView.as_view(ordering=['-CATEGORY']), name="homepage"),
    path('s/', views.BookListView.as_view(ordering=['STATUS']), name="homepage"),
    path('-s/', views.BookListView.as_view(ordering=['-STATUS']), name="homepage"),
    path('cp/', views.BookListView.as_view(ordering=['COPIES']), name="homepage"),
    path('-cp/', views.BookListView.as_view(ordering=['-COPIES']), name="homepage"),
    path('p/', views.BookListView.as_view(ordering=['PRICE']), name="homepage"),
    path('-p/', views.BookListView.as_view(ordering=['-PRICE']), name="homepage"),
    path('', views.BookListView.as_view(), name="homepage"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_request, name="logout"),
    path('login/', views.login_request, name="login"),
    path('profile/', views.profile, name="profile"),
    path('new/', views.BookCreateView.as_view(), name="book-create"),
    path('add/', views.CopyCreateView.as_view(), name="copy-create"),
    path('category/', views.CategoryCreateView.as_view(), name="category-create"),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name="book-update"),
    path('copy/<int:pk>/update/', views.CopyUpdateView.as_view(), name="copy-update"),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name="book-delete"),
    path('copy/<int:pk>/delete/', views.CopyDeleteView.as_view(), name="copy-delete"),
]
