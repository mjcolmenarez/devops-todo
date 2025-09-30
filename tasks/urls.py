from django.urls import path
from .views import (
    TaskList, TaskCreate, TaskUpdate, TaskDelete,
    toggle_done, signup,
)

app_name = "tasks"

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("", TaskList.as_view(), name="list"),
    path("new/", TaskCreate.as_view(), name="create"),
    path("<int:pk>/edit/", TaskUpdate.as_view(), name="update"),
    path("<int:pk>/delete/", TaskDelete.as_view(), name="delete"),
    path("<int:pk>/toggle/", toggle_done, name="toggle"),
]
