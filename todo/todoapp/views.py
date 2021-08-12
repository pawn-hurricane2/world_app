import ipdb
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView, UpdateView
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.response import Response

from .forms import RegistrationForm, LoginForm, ProfilePageForm
from django.shortcuts import HttpResponse
from .models import RegisteredUsers, Todo
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .serializers import CreateTodoSerializer, UpdateTodoSerializer


class IndexView(TemplateView):
    template_name = "todoapp/indexpage.html"


class RegistrationFormView(FormView):
    form_class = RegistrationForm
    template_name = "todoapp/register.html"
    success_url = "/todoapp/login/"

    def form_valid(self, form):
        form.save()
        return super(RegistrationFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = LoginForm
    template_name = "todoapp/login.html"

    def form_valid(self, form):
        user = form.get_authenticated_user()
        login(self.request, user)
        return redirect(reverse('homepage', kwargs={"user_id": user.id}))


class LoginView(LoginFormView):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('homepage', kwargs={"user_id": self.request.user.id}))
        return super(LoginView, self).get(request, *args, **kwargs)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse("index"))


class HomePageView(LoginRequiredMixin, ListView):
    permission_denied_message = "You must be an authenticated user."
    template_name = "todoapp/homepage.html"
    context_object_name = "todo_lists"

    def get_queryset(self):
        # import ipdb;ipdb.set_trace()
        todo_lists = Todo.objects.filter(user_id=self.kwargs.get("user_id"))
        return todo_lists

    def get_context_data(self, *, object_list=None, **kwargs):
        # import ipdb;ipdb.set_trace()
        context = super().get_context_data()
        context.update({"user_id": self.kwargs.get("user_id")})
        return context


class ProfilePageView(LoginRequiredMixin, FormView):
    form_class = ProfilePageForm
    template_name = "todoapp/profile.html"

    def get_user(self):
        user_id = self.kwargs.get("user_id")
        self.user= RegisteredUsers.objects.filter(id=user_id)[0]
        return self.user

    def get_initial(self):
        if self.get_user():
            return {"name": self.user.name, "email": self.user.email, "cell_phone": self.user.cell_phone}
        return super(ProfilePageView, self).get_initial()

    def form_valid(self, form):
        form.save(self.user)
        return redirect(reverse("homepage", kwargs={"user_id": self.user.id}))


class DeleteTodoTask(DestroyAPIView):
    lookup_url_kwarg = "list_id"

    def get_queryset(self):
        # import ipdb;ipdb.set_trace()
        return Todo.objects.filter(user_id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        # import ipdb;ipdb.set_trace()
        super(DeleteTodoTask, self).delete(request, *args, **kwargs)
        return redirect(reverse("homepage", kwargs={"user_id": self.request.user.id}))


class CreateTodoView(TemplateView):
    template_name = "todoapp/create-todo.html"

    def get_context_data(self, **kwargs):
        # import ipdb;ipdb.set_trace()
        context = super().get_context_data(**kwargs)
        context.update({"user_id": kwargs.get("user_id")})
        return context


class CreateTodoTask(CreateAPIView):
    serializer_class = CreateTodoSerializer

    def post(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return redirect(reverse("homepage", kwargs={"user_id": self.request.user.id}))


class UpdateTodoView(TemplateView):
    template_name = "todoapp/update-todo.html"

    def get_object(self):
        user_todo_items = Todo.objects.filter(user_id=self.request.user.id)
        item_to_be_updated = user_todo_items.filter(pk=self.kwargs["list_id"])

        return item_to_be_updated[0] if item_to_be_updated else None

    def get_context_data(self, **kwargs):
        item = self.get_object()
        return {"item": item} if item else {}


class UpdateTodoTask(UpdateAPIView):
    serializer_class = UpdateTodoSerializer
    lookup_url_kwarg = "list_id"

    def get_queryset(self):
        return Todo.objects.filter(user_id=self.request.user.id)

    def post(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return redirect(reverse("homepage", kwargs={"user_id": self.request.user.id}))








