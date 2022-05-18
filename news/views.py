from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрировались")
            return redirect("home")
        else:
            messages.error(request, "Ошибка регистрации")
    else:
        form = UserRegisterForm()
    return render(request, "news/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = UserLoginForm()
    return render(request, "news/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")


class HomeNews(MyMixin, ListView):
    model = News
    template_name = "news/index.html"
    context_object_name = "news"
    mixin_prop = 'Hello world!'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список новостей"
        context["mixin_prop"] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = News
    template_name = "news/index.html"
    context_object_name = "news"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = Category.objects.get(pk=self.kwargs["category_id"])
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True, category_id=self.kwargs["category_id"]).select_related('category')


class ViewNews(DetailView):
    model = News
    pk_url_kwarg = "news_id"
    template_name = "news/view_news.html"
    context_object_name = "news_item"


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = "news/add_news.html"
    # success_url = reverse_lazy('home')
    login_url = "/admin/"

# def index(request):
#     news = News.objects.all()
#     context = {
#         "news": news,
#         "title": "Список новостей"
#     }
#     return render(request, "news/index.html", context)
#
#
# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {
#         "news": news,
#         "category": category
#     }
#     return render(request, "news/category.html", context)
#
#
# def view_news(request, news_id):
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, "news/view_news.html", {"news_item": news_item})
#
#
# def add_news(request):
#     if request.method == "POST":
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, "news/add_news.html", {"form": form})
