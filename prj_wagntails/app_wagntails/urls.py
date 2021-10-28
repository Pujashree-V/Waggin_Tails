from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('owner/', views.ownerPage, name="owner-page"),

    path('account/', views.accountSettings, name="account"),

    path('dogs/', views.dogs, name='dogs'),
    path('owner/<str:pk_test>/', views.owner, name="owner"),
    path('viewVolunteers/<str:pk>/', views.volunteers, name="volunteers"),

    path('create_dog/<str:pk>/', views.createDog, name="create_dog"),
    path('update_dog/<str:pk>/', views.updateDog, name="update_dog"),
    path('delete_dog/<str:pk>/', views.deleteDog, name="delete_dog"),

    ########### Volunteer Related ##########
    path('registerVolunteer/', views.registerVolunteerPage, name="registerVolunteer"),
    path('loginVolunteer/', views.loginVolunteerPage, name="loginVolunteer"),
    path('logoutVolunteer/', views.logoutVolunteerUser, name="logoutVolunteer"),
    path('homeVolunteer', views.homeVolunteer, name="homeVolunteer"),
    path('accountVolunteer/', views.accountSettingsVolunteer, name="accountVolunteer"),
    path('volunteer/', views.volunteerPage, name="volunteer-page"),
    path('volunteer/<str:pk_test>/', views.volunteer, name="volunteer"),
    path('associateVolunteer/<str:pk>/', views.associateVolunteer, name="associateVolunteer"),
]
