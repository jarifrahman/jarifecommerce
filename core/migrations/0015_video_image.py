# Generated by Django 2.2.4 on 2020-10-21 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_video_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
