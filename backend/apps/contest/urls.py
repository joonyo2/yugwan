from django.urls import path
from .views import ContestApplyView, MyApplicationView

urlpatterns = [
    path('apply/', ContestApplyView.as_view(), name='contest-apply'),
    path('my-application/', MyApplicationView.as_view(), name='my-application'),
]
