# Generated by Django 5.0.6 on 2024-09-11 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=30)),
                ('location', models.CharField(max_length=15)),
            ],
        ),
        migrations.RenameField(
            model_name='room',
            old_name='created_At',
            new_name='created_at',
        ),
    ]
