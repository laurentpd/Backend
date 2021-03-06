# Generated by Django 2.0.2 on 2018-03-06 21:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0012_auto_20180306_1604'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='reviewer_of',
            new_name='reviewer',
        ),
        migrations.AddField(
            model_name='solution',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solutions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='solution',
            name='problem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='restapi.Problem'),
        ),
    ]
