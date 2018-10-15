from django.urls import path
from . import views

urlpatterns = [
    path('viewGame/<int:id>', views.viewGame),
    path('viewPlayer/<int:id>', views.viewPlayer),
    path('pop', views.populateDatabase),
    path('newTrick/<int:id>', views.newTrick),
]
