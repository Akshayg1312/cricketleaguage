from django.db import models
from django.contrib.auth.models import User



class Countries(models.Model):
    country_name         = models.CharField(max_length=1000, null=False)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)
    is_active         = models.IntegerField(default=1)


class Teams(models.Model):
    countries_id_fk      = models.ForeignKey(Countries, on_delete=models.CASCADE)
    team_name            = models.CharField(max_length =100)
    total_match_count    =   models.IntegerField(default = 0)
    winning_count           =   models.IntegerField(default = 0)
    losses_count            =   models.IntegerField(default = 0)
    net_run_ret             =   models.FloatField(default  = 0.0)
    points                  =   models.IntegerField(default = 0)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)
    is_active         = models.IntegerField(default=1)


PLAYER_ROLE =(
     ('Batting','Batting'),
     ('Bowling','Bowling'),
     ('Batting/Wk','Batting/Wk'),
)

class PlayerProfile(models.Model):
    team_id_fk           =  models.ForeignKey(Teams, on_delete =models.CASCADE)
    player_name          =  models.CharField(max_length = 100 ,null =True , blank =True)
    player_image         = models.ImageField(upload_to='PlayerImg/',null =True)
    born_date            =  models.DateField(null =True)
    age                  =  models.PositiveIntegerField(default = 0)
    birth_place          =  models.CharField(max_length = 100 ,null=True ,blank =True)
    career_score         =  models.IntegerField(default = 0)
    player_role          =  models.CharField(max_length = 100 ,choices =PLAYER_ROLE,null =True ,blank=True)
    batting_style        =  models.CharField(max_length = 100 ,null=True ,blank =True)
    bowling_style        =  models.CharField(max_length = 100 ,null=True ,blank =True)
    icc_ranking          =  models.IntegerField(default = 0)

    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)
    is_active            = models.IntegerField(default=1)



class Venue(models.Model):
    stadium_name      = models.CharField(max_length = 100 ,null =True)
    country           = models.CharField(max_length =100 , null =True)
    city              = models.CharField(max_length =100  , null=True)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)
    is_active         = models.IntegerField(default=1)


class MatchList(models.Model):
    team_id1_fk       = models.ForeignKey(Teams,on_delete=models.CASCADE,related_name='team1')
    team_id2_fk       = models.ForeignKey(Teams,on_delete=models.CASCADE,related_name='team2')
    Venue_id_fk       = models.ForeignKey(Venue,on_delete=models.CASCADE)
    match_date        = models.DateField(null =True)
    match_time        = models.TimeField(null =True)
    match_status      = models.CharField(max_length =100,default = 'not_complete') #complete/not_complete
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)
    is_active         = models.IntegerField(default=1)


class MatchSummery(models.Model):
    matchlist_id_fk         = models.ForeignKey(MatchList,on_delete = models.CASCADE)
    winner_team_id_fk       = models.ForeignKey(Teams,on_delete = models.CASCADE ,related_name = 'winner_team')
    looser_team_id_fk       = models.ForeignKey(Teams,on_delete = models.CASCADE ,related_name = 'looser_team')
    man_ofthe_match         = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE,related_name = 'man_ofthe_match')
    bowler_ofthe_match      = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE,related_name = 'bowler_ofthe_match')
    best_fielder            = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE,related_name = 'best_fielder')
    win_by                  = models.CharField(max_length =100 ,blank =True ,null =True)
    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)
    is_active               = models.IntegerField(default=1)


class TournamentScoreModel(models.Model):
    team_id_fk              =   models.ForeignKey(Teams,on_delete=models.CASCADE)
    total_match_count       =   models.IntegerField(default = 0)
    winning_count           =   models.IntegerField(default = 0)
    losses_count            =   models.IntegerField(default = 0)
    net_run_ret             =   models.FloatField(default  = 0.0)
    points                  =   models.IntegerField(default = 0)
    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)
    is_active               = models.IntegerField(default=1)




