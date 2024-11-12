from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"), 
    path('job/<str:pk>/', views.job, name="job"),
    path('profile/<int:pk>/', views.userProfile, name="user-profile"),  # Use this path for user profile
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),
    
    path('user/edit/<int:pk>/', views.editProfile, name='edit-profile'),  # Keep the edit profile route separate
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)