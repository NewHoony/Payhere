from django.urls import path
from . import views

app_name="book"

urlpatterns = [
    path("index/", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("detail/<pk>", views.detail, name="detail"),
    path("update/<pk>", views.update, name="update"),
    path("delete/<pk>", views.delete, name="delete"),
    path('duplicate/<pk>', views.duplicate, name='duplicate'),
]