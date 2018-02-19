from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('refs/', views.refs, name='refs'),
    path('personae/', views.personae, name='personae'),
    path('<int:character_id>/', views.persona, name='persona'),
]
