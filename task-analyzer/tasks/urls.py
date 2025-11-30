from django.urls import path
from tasks import views

urlpatterns = [
    path('analyze/', views.analyze_task, name="analyze_tasks"),
    path('suggest/', views.suggest_tasks, name="suggest_tasks"),
]
