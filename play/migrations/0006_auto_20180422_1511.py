# Generated by Django 2.0.4 on 2018-04-22 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('play', '0005_auto_20180422_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='play.Game'),
        ),
    ]
