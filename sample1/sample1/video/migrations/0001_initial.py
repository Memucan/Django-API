# Generated by Django 2.1.4 on 2018-12-15 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videoname', models.CharField(max_length=50)),
                ('videoby', models.CharField(max_length=50)),
            ],
        ),
    ]
