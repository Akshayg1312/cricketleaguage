# Generated by Django 3.2.8 on 2021-10-28 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cricketApp', '0003_rename_palyer_image_playerprofile_player_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerprofile',
            name='team_id_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cricketApp.teams', unique=True),
        ),
    ]
