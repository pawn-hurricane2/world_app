from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegistrationFormView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("homepage/<int:user_id>/", views.HomePageView.as_view(), name="homepage"),
    path("profile/<int:user_id>/", views.ProfilePageView.as_view(), name="profile"),
    path("delete/<int:list_id>/", views.DeleteTodoTask.as_view(), name="delete-todo-task"),
    path("todo-create/<int:user_id>/", views.CreateTodoTask.as_view(), name="create-todo-task"),
    path("create-todo/<int:user_id>/", views.CreateTodoView.as_view(), name="todo-create-view"),
    path("edit-todo-task/<int:list_id>/", views.UpdateTodoTask.as_view(), name="update-todo-task"),
    path("edit-view/<int:list_id>/", views.UpdateTodoView.as_view(), name="update-todo-view"),
]
