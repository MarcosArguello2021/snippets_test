from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from snippets.models import Snippet, Language
from snippets.forms import SnippetForm
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from .tasks import sendEmailInSnippetCreation


class SnippetAdd(LoginRequiredMixin, View):
    def get(self, request):
        form = SnippetForm()
        context = {'form': form, 'action': 'Agregar'}
        return render(request, 'snippets/snippet_add.html', context)

    def post(self, request):
      form = SnippetForm(request.POST)
      if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            if request.user.email:
                sendEmailInSnippetCreation.delay(snippet.name, snippet.description, request.user.email)
            return redirect('index')
      context = {'form': form, 'action': 'Agregar'}
      return render(request, 'snippets/snippet_add.html', context)

class SnippetEdit(LoginRequiredMixin, View):
    def get(self, request, id):
      snippet = get_object_or_404(Snippet, id=id)
      if snippet.user != request.user:
        return redirect('index')
      form = SnippetForm(instance=snippet)
      context = {'form': form, 'action': 'Editar'}
      return render(request, 'snippets/snippet_add.html', context)

    def post(self, request, id):
      snippet = get_object_or_404(Snippet, id=id)
      if snippet.user != request.user:
        return redirect('index')
      form = SnippetForm(request.POST, instance=snippet)
      if form.is_valid():
        form.save()
        return redirect('index')
      context = {'form': form, 'action': 'Editar'}
      return render(request, 'snippets/snippet_add.html', context)

class SnippetDelete(LoginRequiredMixin, View):
    def post(self, request, id):
        snippet = get_object_or_404(Snippet, id=id)
        if snippet.user != request.user:
            return redirect('index')
        snippet.delete()
        return redirect('index')


class SnippetDetails(View):
    def get(self, request, *args, **kwargs):
        snippet_id = self.kwargs["id"]
        snippet = get_object_or_404(Snippet, id=snippet_id)
        if not snippet.public and (not request.user.is_authenticated or snippet.user != request.user):
            return redirect('index')

        lexer = get_lexer_by_name(snippet.language.name)
        formatter = HtmlFormatter(style='friendly')
        highlighted_code = highlight(snippet.snippet, lexer, formatter)

        return render(request, 'snippets/snippet.html', {'snippet': snippet, 'highlighted_code': highlighted_code})


class UserSnippets(View):
    def get(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        user = get_object_or_404(User, username=username)
        if request.user.is_authenticated and request.user == user:
            snippets = Snippet.objects.filter(user=user)
        else:
            snippets = Snippet.objects.filter(user=user, public=True)
        return render(
            request,
            "snippets/user_snippets.html",
            {"snippetUsername": username, "snippets": snippets},
        )


class SnippetsByLanguage(View):
    def get(self, request, *args, **kwargs):
        language_slug = self.kwargs["language"]
        language = get_object_or_404(Language, slug=language_slug)
        snippets = Snippet.objects.filter(language=language, public=True)
        return render(request, "snippets/snippets_by_language.html", {"snippets": snippets, "language": language})


class Login(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'snippets/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index') 
        return render(request, 'snippets/login.html', {'form': form, 'error': 'Invalid credentials'})
    
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('index') 


class Index(View):
    def get(self, request, *args, **kwargs):
        snippets = Snippet.objects.filter(public=True)
        return render(request, "index.html", {"snippets": snippets})