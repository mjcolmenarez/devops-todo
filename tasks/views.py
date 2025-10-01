from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Task
from .forms import TaskForm


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/list.html"

    def get_queryset(self):
        qs = Task.objects.filter(user=self.request.user)
        status = self.request.GET.get("status")
        priority = self.request.GET.get("priority")
        ttype = self.request.GET.get("type")

        if status in {"not_started", "in_progress", "done"}:
            qs = qs.filter(status=status)
        if priority in {"low", "medium", "high"}:
            qs = qs.filter(priority=priority)
        if ttype in {"homework", "work", "personal", "other"}:
            qs = qs.filter(task_type=ttype)

        return qs


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/form.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/form.html"
    success_url = reverse_lazy("tasks:list")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/confirm_delete.html"
    success_url = reverse_lazy("tasks:list")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


@login_required
def toggle_done(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        # flip done and keep status in sync
        new_val = not task.is_done
        task.is_done = new_val
        task.status = Task.STATUS_DONE if new_val else Task.STATUS_NOT_STARTED
        task.save(update_fields=["is_done", "status", "updated_at"])
    return redirect("tasks:list")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
