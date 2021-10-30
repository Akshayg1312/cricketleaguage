
from django.db.models import fields
from .models import *
from rest_framework import serializers

#from api_user_two.models import  *


class CountriesSerializers(serializers.ModelSerializer):

    class Meta:
        model  = Countries
        fields = '__all__'


class TeamSerializers(serializers.ModelSerializer):
    countries_id_fk = CountriesSerializers(read_only=True, many=False)
    class Meta:
        model  = Teams
        fields = '__all__'



class PlayerSerializers(serializers.ModelSerializer):
    team_id_fk = TeamSerializers(read_only=True, many=False)
    class Meta:
        model  = PlayerProfile
        fields = '__all__'


class TeamPlayersSerializer(serializers.ModelSerializer):
    team_id = serializers.CharField(source='team_id1')
    team_name = serializers.CharField(source='team_name1')
    player_image = serializers.CharField(source='player_image1')
    class Meta:
        model  = PlayerProfile
        fields = ('id', 'team_id', 'team_name','player_name','player_image','born_date','age','birth_place','career_score','player_role','batting_style','bowling_style','icc_ranking')


class VenueSerializers(serializers.ModelSerializer):
    class Meta:
        model  = Venue
        fields = '__all__'

class CountrySeriallizerForMatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Countries
        fields  = ['id','country_name']


class TeamsSerializersForMatchSerializer(serializers.ModelSerializer):
    countries_id_fk = CountrySeriallizerForMatchListSerializer(many=False, read_only=True)
    class Meta:
        model  = Teams
        fields = ['id','countries_id_fk','team_name']

class MatchListSerializers(serializers.ModelSerializer):
    team_id1_fk = TeamsSerializersForMatchSerializer(read_only=True, many=False)
    team_id2_fk = TeamsSerializersForMatchSerializer(read_only=True, many=False)
    Venue_id_fk = VenueSerializers(read_only=True, many=False)
    # team1_id = serializers.CharField(source='team1_id1')
    # team_name1_country_name1 = serializers.CharField(source='team_name1_country_name')
    # team_id = serializers.CharField(source='team_id1')
    class Meta:
        model   =  MatchList
        fields  =  '__all__'

class PlayerSerializersForMatchSummery(serializers.ModelSerializer):
    class Meta:
        model   =  PlayerProfile
        fields  =  ['id','player_name'] 
class TeamSerializersForMatchSummery(serializers.ModelSerializer):
    class Meta:
        model  =  Teams
        fields =   ['id','team_name']

class MatchSummerySerializers(serializers.ModelSerializer):
    winner_team_id_fk = TeamSerializersForMatchSummery(read_only=True, many=False)
    looser_team_id_fk = TeamSerializersForMatchSummery(read_only=True, many=False)
    man_ofthe_match = PlayerSerializersForMatchSummery(read_only=True, many=False)
    bowler_ofthe_match = PlayerSerializersForMatchSummery(read_only=True, many=False)
    best_fielder = PlayerSerializersForMatchSummery(read_only=True, many=False)
    class Meta:
        model   =   MatchSummery
        fields  =   '__all__'


class PoiintTableSerializers(serializers.ModelSerializer):
    class Meta:
        model   =   Teams
        fields  =   ['id','team_name','total_match_count','winning_count','losses_count','points','net_run_ret']
