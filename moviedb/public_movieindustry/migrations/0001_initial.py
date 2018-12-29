# Generated by Django 2.1.4 on 2018-12-28 12:00

from django.db import migrations, models
import tenant_schemas.postgresql_backend.base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='industryname',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_url', models.CharField(max_length=128, unique=True)),
                ('schema_name', models.CharField(max_length=63, unique=True, validators=[tenant_schemas.postgresql_backend.base._check_schema_name])),
                ('movieindustryname', models.CharField(max_length=100)),
                ('website', models.CharField(max_length=100)),
                ('phonenumber', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'industryname_table',
            },
        ),
    ]