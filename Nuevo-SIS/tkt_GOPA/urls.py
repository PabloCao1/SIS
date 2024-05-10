from django.urls import path
from .views import *

urlpatterns = [
    path("agregar", TicketGOPACreateView.as_view(), name="tktGOPA_add"),
    path("listar", TicketGOPAListView.as_view(), name="tktGOPA_list"),
    path("ver/<pk>", TicketGOPADetailView.as_view(), name="tktGOPA_detail"),
    path("modificar/<pk>", TicketGOPAUpdateView.as_view(), name="tktGOPA_change"),
    path("eliminar/<pk>", TicketGOPADeleteView.as_view(), name="tktGOPA_delete"),
]