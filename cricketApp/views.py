
from django.conf import settings


# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import QueryDict

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status

from rest_framework import generics, permissions
import random

from django.db.models import F
from django.db.models import Q
from django.db.models import Sum
from django.contrib.auth import authenticate

# model and serializer importing
from .models import *

from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication



response = dict()


# Login API

class LoginView(generics.GenericAPIView):
    def post(self,request):
        if (request.data.get('user_name') != None and request.data.get('user_name') and request.data.get('password')  and request.data.get('password')):
            user_name = request.data.get('user_name')
            password = request.data.get('password')

            
            user = authenticate(username=user_name, password=password)
            # user = User.objects.filter(username =user_name,password =password)
            print(user.id)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                payload = {
                    'user_id':user.id,
                    'user_name':user.username
                }
                response['payload'] = payload
                response['refresh']= str(refresh)
                response['access']= str(refresh.access_token)
                
            else:
                
            
                response['status'] = 'false'
                response['login'] = 'Login Fail'
            return Response(response)



########### Start API  for Country Related   ################

class AddCountries(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    def post(self, request):
        if (request.data.get('country_name') != None and request.data.get('country_name') != ''):
            try:
                country_name = request.data.get('country_name')

                

                
                data = Countries.objects.create(country_name = country_name)
                response['status'] = "true"
                response['message'] = "data added "
                response['country_id'] = data.id
            
            except:
                response['status'] = "false"
                response['message'] = "no data found"

        else:
            response['status'] = "false"
            response['message'] = "no data found"

        return Response(response)


class GetAllCountries(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
    
        try:
            country_data = Countries.objects.all()
            if country_data.exists():
                data = CountriesSerializers(country_data, many=True).data
                response['status'] = "true"
                response['message'] = "data found"
                response['data'] = data
            else:
                response['status'] = "false"
                response['message'] = "no data found"
        except:
            response['status'] = "false"
            response['message'] = "no data found"


        return Response(response)

    

class GetCountryById(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if (request.data.get('country_id') != None and request.data.get('country_id') != ''):
        
            try:
                country_id = request.data.get('country_id')
                country_data = Countries.objects.get(id =  country_id)
                if country_data:
                    data = CountriesSerializers(country_data, many=False).data
                    response['status'] = "true"
                    response['message'] = "data found"
                    response['data'] = data
                else:
                    response['status'] = "false"
                    response['message'] = "no data found"
            except:
                response['status'] = "false"
                response['message'] = "no data found"
        
        else:
            response['status'] = "false"
            response['message'] = "no required param"

    
        return Response(response)


class EditCountryById(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        if (request.data.get('country_id') != None and request.data.get('country_id') != '' and request.data.get('country_name')!=None and request.data.get('country_name') != ''):
        
            try:
                country_id = request.data.get('country_id')
                country_name = request.data.get('country_name')
                country_data = Countries.objects.get(id =  country_id)
                country_data.country_name = country_name
                country_data.save()
                
                response['status'] = "true"
                response['message'] = "data updated"
                response['country_id'] = country_data.id
                
            except:
                response['status'] = "false"
                response['message'] = "no data found"

        else:
            response['status'] = "false"
            response['message'] = "no required param"


    
        return Response(response)


class DeleteCountry(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        if (request.data.get('country_id') != None and request.data.get('country_id') != ''):
        
            try:
                country_id = request.data.get('country_id')
                
                country_data = Countries.objects.get(id =  country_id)
                
                country_data.delete()
                
                response['status'] = "true"
                response['message'] = "country deleted"
                
                
            except:
                response['status'] = "false"
                response['message'] = "no data found"

        else:
            response['status'] = "false"
            response['message'] = "no required param"

        return Response(response)



########### End API  for Country Related   ################



# ######## Start API  for Teams Related    ################

class AddTeam(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    def post(self,request):
        if (request.data.get('country_id') != None and request.data.get('country_id') != '' and request.data.get('team_name') != None and request.data.get('team_name') != ''):
            try:
                country_id = request.data.get('country_id')
                country    = Countries.objects.get(id= country_id)
                team_name  = request.data.get('team_name')

                data       = Teams.objects.create(countries_id_fk = country ,team_name = team_name)

                response['status'] = "true"
                response['message'] = "data added "
                response['team_id'] = data.id
            
            except:
                response['status'] = "false"
                response['message'] = "no data found"

        else:
            response['status'] = "false"
            response['message'] = "no data found"

        return Response(response)



class GetAllTeam(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
    
        try:
            team_data = Teams.objects.all()
            if team_data.exists():
                data = TeamSerializers(team_data, many=True).data
                response['status'] = "true"
                response['message'] = "data found"
                response['data'] = data
            else:
                response['status'] = "false"
                response['message'] = "no data found"
        except:
            response['status'] = "false"
            response['message'] = "no data found"


        return Response(response)


class GetTeamById(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if (request.data.get('team_id') != None and request.data.get('team_id') != ''):
        
            try:
                team_id = request.data.get('team_id')
                team_data = Teams.objects.get(id =  team_id)
                if team_data:
                    data = TeamSerializers(team_data, many=False).data
                    response['status'] = "true"
                    response['message'] = "data found"
                    response['data'] = data
                else:
                    response['status'] = "false"
                    response['message'] = "no data found"
            except:
                response['status'] = "false"
                response['message'] = "no data found"
        
        else:
            response['status'] = "false"
            response['message'] = "no required param"

    
        return Response(response)



class EditTeam(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        if (request.data.get('team_id') != None and request.data.get('team_id') != '' and request.data.get('team_name')!=None and request.data.get('team_name') != ''):
        
            try:
                team_id = request.data.get('team_id')
                team_name = request.data.get('team_name')
                Team_data = Teams.objects.get(id = team_id)
                Team_data.team_name = team_name
                Team_data.save()
                
                response['status'] = "true"
                response['message'] = "data updated"
                response['country_id'] = Team_data.id
                
            except:
                response['status'] = "false"
                response['message'] = "no data found"

        else:
            response['status'] = "false"
            response['message'] = "no required param"


    
        return Response(response)


class DeleteTeam(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    def post(self, request):
        if (request.data.get('team_id') != None and request.data.get('team_id') != ''):
        
            try:
                team_id = request.data.get('team_id')
                
                team = Teams.objects.get(id =  team_id)
                
                team.delete()
                
                response['status'] = "true"
                response['message'] = "Team deleted"
                
                
            except:
                response['status'] = "false"
                response['message'] = "no data found"

        else:
            response['status'] = "false"
            response['message'] = "no required param"

        return Response(response)


########## End Teams API #######################

########## Start PlayerProfile API  ############

class AddPlayerProfile(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    def post(self ,request):
        if (request.data.get('team_id') != None and request.data.get('team_id') != '' and request.data.get('player_name') != None  and request.data.get('player_name') != ''  and request.data.get('born_date') != None  and request.data.get('born_date') != ''  and request.data.get('age') != None and request.data.get('age') != '' and request.data.get('player_role') != None and  request.data.get('player_role') != '' and request.data.get('batting_style') != None and request.data.get('batting_style') != '' and request.data.get('bowling_style') != None and request.data.get('bowling_style') != '' ):

            team_id = request.data.get('team_id')
            team    = Teams.objects.get(id = team_id)
            player_name = request.data.get('player_name')
            player_image = request.data.get('player_image')
            born_date = request.data.get('born_date')
            age = request.data.get('age')
            birth_place = request.data.get('birth_place')
            career_score = request.data.get('career_score')
            player_role = request.data.get('player_role')
            batting_style = request.data.get('batting_style')
            bowling_style = request.data.get('bowling_style')
            icc_ranking = request.data.get('icc_ranking')
            
            data  = PlayerProfile.objects.create(team_id_fk = team , player_name = player_name ,player_image = player_image ,born_date = born_date ,age = age , birth_place = birth_place, career_score= career_score , player_role = player_role , batting_style = batting_style ,bowling_style = bowling_style , icc_ranking = icc_ranking)

            response['status'] = "true"
            response['message'] = "data added "
            response['player_id'] = data.id

        else:
            response['status'] = "false"
            response['message'] = "no required param "

        return Response(response)



class GetAllPlayer(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
    
        try:
            players = PlayerProfile.objects.all()
            if players.exists():
                data = PlayerSerializers(players, many=True).data
                response['status'] = "true"
                response['message'] = "data found"
                response['data'] = data
            else:
                response['status'] = "false"
                response['message'] = "no data found"
        except:
            response['status'] = "false"
            response['message'] = "no data found"


        return Response(response)


class GetPlayerById(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if (request.data.get('player_id') != None and request.data.get('player_id') != ''):
        
            try:
                player_id = request.data.get('player_id')
                player_data = PlayerProfile.objects.get(id =  player_id)
                if player_data:
                    data = PlayerSerializers(player_data, many=False).data
                    response['status'] = "true"
                    response['message'] = "data found"
                    response['data'] = data
                else:
                    response['status'] = "false"
                    response['message'] = "no data found"
            except:
                response['status'] = "false"
                response['message'] = "no data found"
        
        else:
            response['status'] = "false"
            response['message'] = "no required param"

    
        return Response(response)


class GetTeamPlayers(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if (request.data.get('team_id') != None and request.data.get('team_id') != ''):
        
            try:
                team_id = request.data.get('team_id')
                teams = Teams.objects.get(id =  team_id)
                # players = PlayerProfile.objects.filter(team_id_fk =teams,is_active = 1)
                players = PlayerProfile.objects.filter(team_id_fk =teams,is_active = 1).values('id', 'team_id_fk__id','team_id_fk__team_name', 'player_name', 'player_image','born_date','age','birth_place','career_score','player_role','batting_style','bowling_style','icc_ranking').annotate(team_id1=F('team_id_fk__id'), team_name1 = F('team_id_fk__team_name'),player_image1=F('player_image'))
                if players.exists():
                    data = TeamPlayersSerializer(players, many=True).data
                    
                    response['status'] = "true"
                    response['message'] = "data found"
                    response['data'] = data
                else:
                    response['status'] = "false"
                    response['message'] = "no data found"
            except:
                response['status'] = "false"
                response['message'] = "no data found"
        
        else:
            response['status'] = "false"
            response['message'] = "no required param"

    
        return Response(response)






class EditPlayerProfile(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    def post(self ,request):
        if (request.data.get('player_id') != None and request.data.get('player_id') != '' ):
            
            player_id = request.data.get('player_id')
            player    = PlayerProfile.objects.get(id = player_id)
            print(player.player_image)
            team_id = request.data.get('team_id',player.team_id_fk.id)
            team    = Teams.objects.get(id = team_id)
            player_name = request.data.get('player_name',player.player_name)
            player_image = request.data.get('player_image',player.player_image)
            born_date = request.data.get('born_date',player.born_date)
            age = request.data.get('age',player.age)
            birth_place = request.data.get('birth_place',player.birth_place)
            career_score = request.data.get('career_score',player.career_score)
            player_role = request.data.get('player_role',player.player_role)
            print(player_role)
            batting_style = request.data.get('batting_style',player.batting_style)
            bowling_style = request.data.get('bowling_style',player.bowling_style)
            icc_ranking = request.data.get('icc_ranking',player.icc_ranking)
            
            

            player.team_id_fk = team
            player.player_name = player_name
            player.player_image = player_image
            player.born_date = born_date
            player.age = age
            player.birth_place = birth_place
            player.career_score = career_score
            player.player_role = player_role
            player.batting_style = batting_style

            player.bowling_style = bowling_style
            player.icc_ranking = icc_ranking

            player.save()


            response['status'] = "true"
            response['message'] = "data Updated "
            response['player_id'] = player.id

        else:
            response['status'] = "false"
            response['message'] = "no required param "

        return Response(response)



class DeletePlayer(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        if (request.data.get('player_id') != None and request.data.get('player_id') != ''):
        
            try:
                player_id = request.data.get('player_id')
                
                player = PlayerProfile.objects.get(id = player_id )
                
                player.delete()
                
                response['status'] = "true"
                response['message'] = "Player Profile deleted"
                
                
            except:
                response['status'] = "false"
                response['message'] = "no data found"

        else:
            response['status'] = "false"
            response['message'] = "no required param"

        return Response(response)






##### Add Venue  #######################

class AddVenue(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    def post(self,request):
        if (request.data.get('stadium_name') != None and request.data.get('stadium_name') != '' and request.data.get('country') != None and request.data.get('country') != '' and request.data.get('city') != None and request.data.get('city') != ''):
            try:
                stadium_name = request.data.get('stadium_name')
                country = request.data.get('country')
                city = request.data.get('city')
                

                data       = Venue.objects.create(stadium_name = stadium_name ,country = country,city=city)

                response['status'] = "true"
                response['message'] = "data added "
                response['team_id'] = data.id
            
            except:
                response['status'] = "false"
                response['message'] = "no data found"

        else:
            response['status'] = "false"
            response['message'] = "no data found"

        return Response(response)




class GetAllVenue(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            Venues = Venue.objects.all()
            if Venues.exists():
                data = VenueSerializers(Venues, many=True).data
                response['status'] = "true"
                response['message'] = "data found"
                response['data'] = data
            else:
                response['status'] = "false"
                response['message'] = "no data found"
        except:
            response['status'] = "false"
            response['message'] = "no data found"


        return Response(response)




class GetVenueById(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if (request.data.get('venue_id') != None and request.data.get('venue_id') != ''):
        
            try:
                venue_id = request.data.get('venue_id')
                venue_data = Venue.objects.get(id =  venue_id)
                if venue_data:
                    data = VenueSerializers(venue_data, many=False).data
                    response['status'] = "true"
                    response['message'] = "data found"
                    response['data'] = data
                else:
                    response['status'] = "false"
                    response['message'] = "no data found"
            except:
                response['status'] = "false"
                response['message'] = "no data found"
        
        else:
            response['status'] = "false"
            response['message'] = "no required param"

    
        return Response(response)



class EditVenue(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        if (request.data.get('venue_id') != None and request.data.get('venue_id') != '' ):
        
            try:
                venue_id = request.data.get('venue_id')
                venue_data = Venue.objects.get(id = venue_id)
                stadium_name = request.data.get('stadium_name',venue_data.stadium_name)
                country = request.data.get('country',venue_data.country)
                city = request.data.get('city',venue_data.city)
                
                
                venue_data.stadium_name = stadium_name
                venue_data.country = country
                venue_data.city = city
                venue_data.save()
                
                response['status'] = "true"
                response['message'] = "data updated"
                response['country_id'] = venue_data.id
                
            except:
                response['status'] = "false"
                response['message'] = "no data found"

        else:
            response['status'] = "false"
            response['message'] = "no required param"


    
        return Response(response)


class DeleteVenue(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    def post(self, request):
        if (request.data.get('venue_id') != None and request.data.get('venue_id') != ''):
        
            try:
                venue_id = request.data.get('venue_id')
                
                venue = Venue.objects.get(id = venue_id )
                
                venue.delete()
                
                response['status'] = "true"
                response['message'] = "Venue deleted"
                
                
            except:
                response['status'] = "false"
                response['message'] = "no data found"

        else:
            response['status'] = "false"
            response['message'] = "no required param"

        return Response(response)


############### End Venue ##############


########## Add MatchList  #############

class AddMatch(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    def post(self,request):
        if (request.data.get('team1_id') != None and request.data.get('team1_id') != '' and request.data.get('team2_id') != None and request.data.get('team2_id') != '' and request.data.get('venue_id') != None and request.data.get('venue_id') != '' and request.data.get('match_date') != None and request.data.get('match_date') != '' and request.data.get('match_time') != None and request.data.get('match_time') != ''):
            try:
                team1_id = request.data.get('team1_id')
                team1    = Teams.objects.get(id = team1_id)
                team2_id = request.data.get('team2_id')
                team2    = Teams.objects.get(id = team2_id)
                venue_id = request.data.get('venue_id')
                venue    = Venue.objects.get(id = venue_id)
                match_date = request.data.get('match_date')
                match_time = request.data.get('match_time')
                

                data       = MatchList.objects.create(team_id1_fk = team1 ,team_id2_fk = team2,Venue_id_fk=venue,match_date=match_date,match_time=match_time)

                response['status'] = "true"
                response['message'] = "data added "
                response['team_id'] = data.id
            
            except:
                response['status'] = "false"
                response['message'] = "no data found"

        else:
            response['status'] = "false"
            response['message'] = "no data found"

        return Response(response)



class GetAllMatchList(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            # match_list = MatchList.objects.values('id', 'team_id1_fk__id','team_id1_fk__countries_id_fk__country_name').annotate(team1_id1=F('team_id1_fk__id'), team_name1_country_name = F('team_id1_fk__countries_id_fk__country_name'))
            match_list = MatchList.objects.all()
            if match_list.exists():
                data = MatchListSerializers(match_list, many=True).data
                response['status'] = "true"
                response['message'] = "data found"
                response['data'] = data
            else:
                response['status'] = "false"
                response['message'] = "no data found"
        except:
            response['status'] = "false"
            response['message'] = "no data found"


        return Response(response)


class AddMatchSummery(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    def post(self,request):
        if (request.data.get('match_list_id') != None and request.data.get('match_list_id') != '' and request.data.get('winner_team_id') != None and request.data.get('winner_team_id') != '' and request.data.get('looser_team_id') != None and request.data.get('looser_team_id') != '' and request.data.get('man_ofthe_match_id') != None and request.data.get('man_ofthe_match_id') != '' and request.data.get('bowler_ofthe_match_id') != None and request.data.get('bowler_ofthe_match_id') != ''  and request.data.get('best_fielder_id') != None and request.data.get('best_fielder_id') != '' and request.data.get('win_by') != None and request.data.get('win_by') != ''):
            try:
                match_list_id = request.data.get('match_list_id')
                match_list    = MatchList.objects.get(id = match_list_id)

                winner_team_id = request.data.get('winner_team_id')
                winner_team    = Teams.objects.get(id = winner_team_id)

                looser_team_id = request.data.get('looser_team_id')
                looser_team    = Teams.objects.get(id = looser_team_id)

                man_ofthe_match_id = request.data.get('man_ofthe_match_id')
                man_ofthe_match    = PlayerProfile.objects.get(id = man_ofthe_match_id)
                
                
                bowler_ofthe_match_id = request.data.get('bowler_ofthe_match_id')
                bowler_ofthe_match    = PlayerProfile.objects.get(id = bowler_ofthe_match_id)
                
                best_fielder_id = request.data.get('best_fielder_id')
                best_fielder    = PlayerProfile.objects.get(id = best_fielder_id)

                win_by = request.data.get('win_by','0')
                

                data       = MatchSummery.objects.create(matchlist_id_fk = match_list ,winner_team_id_fk = winner_team,looser_team_id_fk=looser_team,man_ofthe_match=man_ofthe_match,bowler_ofthe_match=bowler_ofthe_match,best_fielder=best_fielder,win_by=win_by)

                #Total Match Count
                winner_team.total_match_count +=1
                looser_team.total_match_count +=1

                #Total Winning Count
                winner_team.winning_count  +=1

                #Total Loss Count
                looser_team.losses_count  +=1

                # Points

                winner_team.points         += 2

                winner_team.save()
                looser_team.save()






                response['status'] = "true"
                response['message'] = "data added "
                response['team_id'] = data.id
            
            except:
                response['status'] = "false"
                response['message'] = "no data found"

        else:
            response['status'] = "false"
            response['message'] = "no data found"
        return Response(response)



class GetAllAddMatchSummery(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            match_summery = MatchSummery.objects.all()
            
            if match_summery.exists():
                data = MatchSummerySerializers(match_summery, many=True).data
                response['status'] = "true"
                response['message'] = "data found"
                response['data'] = data
            else:
                response['status'] = "false"
                response['message'] = "no data found"
        except:
            response['status'] = "false"
            response['message'] = "no data found"


        return Response(response)



# Point Table
class GetTournamentScoreTable(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            pointtable = Teams.objects.filter(is_active = 1).values('id','team_name','total_match_count','winning_count','losses_count','points','net_run_ret')
            
            if pointtable.exists():
                data = PoiintTableSerializers(pointtable, many=True).data
                response['status'] = "true"
                response['message'] = "data found"
                response['data'] = data
            else:
                response['status'] = "false"
                response['message'] = "no data found"
        except:
            response['status'] = "false"
            response['message'] = "no data found"


        return Response(response)








