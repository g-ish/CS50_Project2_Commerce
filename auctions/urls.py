from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("close_listing/<str:action>/<int:pk>", views.close_listing, name="close_listing"),
    path('my_listings', views.view_user_listings, name="user_listings"),
    path('past_listings', views.view_past_listings, name="past_listings"),
    path('listings/<int:pk>', views.view_listing, name="view_listing"),
    path('listing/<int:pk>/new_comment', views.new_comment, name="new_comment"),
    path('my_watchlist', views.my_watchlist, name="my_watchlist"),
    path('add_watchlist/<int:pk>', views.add_watchlist, name="add_watchlist"),
    path('delete_watchlist/<int:pk>', views.delete_watchlist, name="delete_watchlist"),
    path('category_filter', views.category_filter, name="category_filter"),
]
