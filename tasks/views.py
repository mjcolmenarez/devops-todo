from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import TaskForm, TodoListForm
from .models import Task, TodoList


# Allow GET logout so the menu link works (no 405).
def logout_view(request):
    logout(request)
    return redirect("login")


# ------------------ Tasks ------------------ #
class TaskList(LoginRequiredMixin, ListView):
    template_name = "tasks/list.html"
    model = Task
    context_object_name = "object_list"

    def get_queryset(self):
        qs = Task.objects.filter(user=self.request.user)

        status = self.request.GET.get("status")
        if status in {"not_started", "in_progress", "done"}:
            qs = qs.filter(status=status)

        list_id = self.request.GET.get("list")
        if list_id:
            qs = qs.filter(todo_list_id=list_id)

        # IMPORTANT: No "is_done" here
        return qs.order_by("status", "due_date", "title")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["lists"] = TodoList.objects.filter(user=self.request.user).order_by("name")
        ctx["active_list_id"] = self.request.GET.get("list", "")
        ctx["page_title"] = "To-do List"
        return ctx


class TaskCreate(LoginRequiredMixin, CreateView):
    template_name = "tasks/form.html"
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    template_name = "tasks/form.html"
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:list")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskDelete(LoginRequiredMixin, DeleteView):
    template_name = "tasks/confirm_delete.html"
    model = Task
    success_url = reverse_lazy("tasks:list")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


@require_POST
def toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.status = "not_started" if task.status == "done" else "done"
    task.save(update_fields=["status"])
    # preserve filters if you had any in the query string
    qs = request.META.get("QUERY_STRING", "")
    return redirect(f"/?{qs}" if qs else reverse_lazy("tasks:list"))


# ------------------ Lists (Collections) ------------------ #
class ListList(LoginRequiredMixin, ListView):
    template_name = "tasks/lists.html"
    model = TodoList
    context_object_name = "lists"

    def get_queryset(self):
        # IMPORTANT: order by 'name', not any removed columns
        return TodoList.objects.filter(user=self.request.user).order_by("name")


class ListCreate(LoginRequiredMixin, CreateView):
    template_name = "tasks/list_form.html"
    model = TodoList
    form_class = TodoListForm
    success_url = reverse_lazy("tasks:lists")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ListUpdate(LoginRequiredMixin, UpdateView):
    template_name = "tasks/list_form.html"
    model = TodoList
    form_class = TodoListForm
    success_url = reverse_lazy("tasks:lists")

    def get_queryset(self):
        return TodoList.objects.filter(user=self.request.user)


class ListDelete(LoginRequiredMixin, DeleteView):
    template_name = "tasks/list_confirm_delete.html"
    model = TodoList
    success_url = reverse_lazy("tasks:lists")

    def get_queryset(self):
        return TodoList.objects.filter(user=self.request.user)
