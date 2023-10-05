from django.urls import path

from .views import MemberPassbook, SplitAPIView

urlpatterns = [
    path("split", SplitAPIView.as_view(), name="split"),
    path("passbook", MemberPassbook.as_view(), name="passbook"),
]
