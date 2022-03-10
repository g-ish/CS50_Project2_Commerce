from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path('my_listings', views.view_user_listings, name="user_listings"),
    path('past_listings', views.view_past_listings, name="past_listings"),
    path('listings/<int:pk>', views.view_listing, name="view_listing")
]
