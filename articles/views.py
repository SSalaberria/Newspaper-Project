from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from .forms import CommentForm
from .models import Article, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "article_list.html"
    login_url = 'login'  # override LoginRequiredMixin default parameter
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment_parent = Article.objects.get(id=request.POST['article_id'])
            new_comment = Comment(article=comment_parent, comment=request.POST['comment'], author=self.request.user)
            new_comment.save()
        return HttpResponseRedirect('/articles/')


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "article_detail.html"
    login_url = 'login'


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "article_create.html"
    fields = ['title', 'body', ]
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Article
    fields = ['title', 'body', ]
    template_name = "article_edit.html"
    login_url = 'login'

    def test_func(self):
        return self.get_object().author == self.request.user  # Returns 403 if author != authenticated user


class ArticleDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    login_url = 'login'
    success_url = reverse_lazy("article_list")

    def test_func(self):
        return self.get_object().author == self.request.user
