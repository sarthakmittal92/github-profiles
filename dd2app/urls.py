from django.urls import path

from dd2app.views import ProfileList, ProfileData, SignUpView, UpdateNow

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<string>/', ProfileData, name='profiledata'),
    path('explore/', ProfileList, name='profilelist'),
    path('update/<string>/', UpdateNow, name='update'),
]