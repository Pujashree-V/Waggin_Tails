from django.conf.urls import include
from django.urls import path
from django.conf.urls import handler404, handler400, handler403, handler500

from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('loginOwner/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('baseLogin/', views.baseLogin, name="baseLogin"),
    path('owner/', views.ownerPage, name="owner-page"),

    path('account/', views.accountSettings, name="account"),
    path('ownerDashboard/', views.ownerDashboard, name="ownerDashboard"),
    path('volunteerDashboard/', views.volunteerDashboard,
         name="volunteerDashboard"),

    path('dogs/<str:pk>/', views.dogs, name='dogs'),
    path('owner/<str:pk_test>/', views.owner, name="owner"),
    path('viewVolunteers/<str:pk>/', views.volunteers, name="volunteers"),

    path('create_dog/<str:pk>/', views.createDog, name="create_dog"),
    path('update_dog/<str:pk>/', views.updateDog, name="update_dog"),
    path('delete_dog/<str:pk>/', views.deleteDog, name="delete_dog"),
    path('addlocation/<str:pk>/', views.addDateLocation, name="date-location"),
    path('updatelocation/<str:pk>/<str:pk_test>',
         views.updateDateLocation, name="update-location"),
    path('deletelocation/<str:pk>/<str:pk_test>',
         views.deleteDateLocation, name="delete-location"),
    path('addplaydate/<str:pk>/', views.addPlayDate, name="play-date"),
    path('error/<str:pk>/', views.error, name="error"),

    ########### Volunteer Related ##########
    path('registerVolunteer/', views.registerVolunteerPage,
         name="registerVolunteer"),
    path('loginVolunteer/', views.loginVolunteerPage, name="loginVolunteer"),
    path('logoutVolunteer/', views.logoutVolunteerUser, name="logoutVolunteer"),
    path('homeVolunteer/', views.homeVolunteer, name="homeVolunteer"),
    path('accountVolunteer/', views.accountSettingsVolunteer,
         name="accountVolunteer"),
    path('volunteer/', views.volunteerPage, name="volunteer-page"),
    path('volunteer/<str:pk_test>/', views.volunteer, name="volunteer"),
    path('associateVolunteer/<str:pk>/',
         views.associateVolunteer, name="associateVolunteer"),

    ########### Chat Related ##########
    path('chat/<str:pk>/', views.chat_view, name='chats'),
    path('chatMessage/<str:sender>/<str:receiver>/<str:pk>/',
         views.message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>/',
         views.message_list, name='message-detail'),
    path('api/messages/', views.message_list, name='message-list'),
    path('chatMessageSubmit/<int:sender>/<int:receiver>/',
         views.chatMessageSubmit, name='chatSubmit'),

    ########### volunteer chat Related ##########
    path('volunteerChat/<str:pk>/',
         views.volunteer_chat_view, name='volunteerChats'),
    path('volunteerChatMessage/<str:sender>/<str:receiver>/<str:pk>/',
         views.volunteer_message_view, name='volunteerChat'),

]
