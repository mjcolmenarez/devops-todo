from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    # Tasks
    path("", views.TaskList.as_view(), name="list"),
    path("new/", views.TaskCreate.as_view(), name="create"),
    path("edit/<int:pk>/", views.TaskUpdate.as_view(), name="update"),
    path("delete/<int:pk>/", views.TaskDelete.as_view(), name="delete"),
    path("toggle/<int:pk>/", views.toggle, name="toggle"),

    # Lists (collections)
    path("lists/", views.ListList.as_view(), name="lists"),
    path("lists/new/", views.ListCreate.as_view(), name="list_create"),
    path("lists/<int:pk>/edit/", views.ListUpdate.as_view(), name="list_update"),
    path("lists/<int:pk>/delete/", views.ListDelete.as_view(), name="list_delete"),
]

