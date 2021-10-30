from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    # Country Related API
    path('login', LoginView.as_view(), name="login"),
    path('addCountries', AddCountries.as_view(), name="addCountries"),
    path('getAllCountries', GetAllCountries.as_view(), name="getAllCountries"),
    path('getCountryById', GetCountryById.as_view(), name="getCountryById"),
    path('editCountryById', EditCountryById.as_view(), name="editCountryById"),
    path('deleteCountry', DeleteCountry.as_view(), name="deleteCountry"),

    # Teams Realated API

    path('addTeam', AddTeam.as_view(), name="addTeam"),
    path('getAllTeam', GetAllTeam.as_view(), name="getAllTeam"),
    path('getTeamById', GetTeamById.as_view(), name="getTeamById"),
    path('editTeam', EditTeam.as_view(), name="editTeam"),
    path('deleteTeam', DeleteTeam.as_view(), name="deleteTeam"),

    # Player Profile
    path('addPlayerProfile', AddPlayerProfile.as_view(), name="addPlayerProfile"),
    path('getAllPlayer', GetAllPlayer.as_view(), name="getAllPlayer"), 
    path('getPlayerById', GetPlayerById.as_view(), name="getPlayerById"),
    path('getTeamPlayers', GetTeamPlayers.as_view(), name="getTeamPlayers"),
    path('editPlayerProfile', EditPlayerProfile.as_view(), name="editPlayerProfile"),
    path('deletePlayer', DeletePlayer.as_view(), name="deletePlayer"),

    # Venue Related API
    path('addVenue', AddVenue.as_view(), name="addVenue"),
    path('getAllVenue', GetAllVenue.as_view(), name="getAllVenue"),
    path('getVenueById', GetVenueById.as_view(), name="getVenueById"),
    path('editVenue', EditVenue.as_view(), name="editVenue"),
    path('deleteVenue', DeleteVenue.as_view(), name="deleteVenue"),
    path('addMatch', AddMatch.as_view(), name="addMatch"),
    path('getAllMatchList', GetAllMatchList.as_view(), name="getAllMatchList"),
    path('addMatchSummery', AddMatchSummery.as_view(), name="addMatchSummery"),
    path('getAllAddMatchSummery', GetAllAddMatchSummery.as_view(), name="getAllAddMatchSummery"),


    #PointTable
    path('getTournamentScoreTable', GetTournamentScoreTable.as_view(), name="getTournamentScoreTable"),
    
    
    
    
    
    
]