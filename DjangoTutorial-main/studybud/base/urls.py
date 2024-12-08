from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"), 
    path('job/<str:pk>/', views.job, name="job"),
    path('profile/<int:pk>/', views.userProfile, name="user-profile"),  
    path('create-Job/', views.createJob, name="create-Job"),
    path('update-job/<str:pk>', views.updateJob, name="update-Job"),
    path('delete-job<str:pk>', views.deleteJob, name="delete-Job"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),
    
    path('user/edit/<int:pk>/', views.editProfile, name='edit-profile'),  
    path('add-job-applied/', views.add_job_applied, name='add-job-applied'),
]
