# Generated by Django 2.0.1 on 2018-04-10 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SLE', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comorbidity',
            fields=[
                ('comorbidityid', models.AutoField(primary_key=True, serialize=False)),
                ('comorbiditytype', models.TextField(blank=True, null=True)),
                ('detail', models.TextField(blank=True, null=True)),
                ('diagnosedate', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'comorbidity',
                'managed': False,
            },
        ),
    ]
