from django.urls import path
from .views import AchatTicketView, PartieDetailView,  PartieListView

urlpatterns = [
    path('parties/', PartieListView.as_view(), name='partie-list'),
    path('parties/<int:pk>/', PartieDetailView.as_view(), name='partie-detail'),
    path('parties/<int:pk>/acheter/', AchatTicketView.as_view(), name="partie-achetere")
]