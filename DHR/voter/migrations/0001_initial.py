# Generated by Django 5.1.2 on 2024-10-18 19:20

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Voter",
            fields=[
                ("VoterID", models.AutoField(primary_key=True, serialize=False)),
                ("government_number", models.BigIntegerField()),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("father_name", models.CharField(max_length=100)),
                ("gender", models.CharField(max_length=10)),
                ("CNIC", models.BigIntegerField(unique=True)),
                ("address", models.TextField()),
                ("mobile_number", models.BigIntegerField()),
                ("family_code", models.BigIntegerField(blank=True, null=True)),
                ("block_number", models.CharField(max_length=50)),
            ],
        ),
    ]
