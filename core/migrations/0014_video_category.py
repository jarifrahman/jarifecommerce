# Generated by Django 2.2.4 on 2020-10-21 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Category'),
        ),
    ]
