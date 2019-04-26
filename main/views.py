from django.shortcuts import render, redirect
# from django.http import HttpResponse
from .models import Category, Book, BookCopy, update
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import NewUserForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class BookListView(ListView):
    model = Book
    template_name = "main/home.html"
    context_object_name = "books"
    ordering = None

    def get_object(self, queryset=None):
        return queryset.get(ordering=self.ordering)


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ["TITLE", "AUTHOR", "DATE", "CATEGORY", "DESCRIPTION", "AUTHOR", "LANGUAGE", "PRICE"]
    success_url = "/"


class CopyCreateView(LoginRequiredMixin, CreateView):
    model = BookCopy
    template_name = "main/book_form.html"
    fields = ["BOOK", "LAST_BORROWER", "LAST_LOANED", "CLASSIFICATION", "STATUS"]
    success_url = "/"


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = "main/book_form.html"
    fields = ["TITLE"]
    success_url = "/"


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ["TITLE", "AUTHOR", "DATE", "CATEGORY", "DESCRIPTION", "AUTHOR", "LANGUAGE", "PRICE"]
    success_url = "/"


class CopyUpdateView(LoginRequiredMixin, UpdateView):
    model = BookCopy
    template_name = "main/book_form.html"
    fields = ["BOOK", "LAST_BORROWER", "LAST_LOANED", "CLASSIFICATION", "STATUS"]
    success_url = "/"


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = "/"


class CopyDeleteView(LoginRequiredMixin, DeleteView):
    model = BookCopy
    success_url = "/"


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = NewUserForm
    return render(request,
                  "main/register.html",
                  context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect("main:homepage")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    form = AuthenticationForm()
    return render(request,
                  "main/login.html",
                  {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, f"Your account has been updated!")
            return redirect("main:homepage")

    form = UserUpdateForm(instance=request.user)
    return render(request,
                  "main/profile.html",
                  context={"form": form})
