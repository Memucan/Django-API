# Generated by Django 2.1.4 on 2018-12-29 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_moviedetails', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='cast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero', models.CharField(max_length=100)),
                ('heroine', models.CharField(max_length=100)),
                ('villain', models.CharField(max_length=100)),
                ('movieid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cast', to='tenant_moviedetails.movie')),
            ],
            options={
                'db_table': 'cast_table',
            },
        ),
    ]
