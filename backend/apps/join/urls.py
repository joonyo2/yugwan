from django.urls import path
from .views import VolunteerApplyView, DonationCreateView

urlpatterns = [
    path('volunteers/apply/', VolunteerApplyView.as_view(), name='volunteer-apply'),
    path('donations/', DonationCreateView.as_view(), name='donation-create'),
]
