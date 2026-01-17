from django.urls import path
from .views import ActivePopupListView

urlpatterns = [
    path('active/', ActivePopupListView.as_view(), name='active-popups'),
]
