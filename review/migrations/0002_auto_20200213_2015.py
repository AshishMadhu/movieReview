# Generated by Django 3.0.3 on 2020-02-13 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ratting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratted', models.IntegerField(choices=[(1, '💥'), (2, '💥💥'), (3, '💥💥💥'), (4, '💥💥💥💥'), (5, '💥💥💥💥💥')], default=0)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='comment_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='reports',
            field=models.ManyToManyField(blank=True, related_name='comment_reports', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='movie',
            name='ratting',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='movie',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='Preview',
        ),
        migrations.AddField(
            model_name='ratting',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_rating', to='review.Movie'),
        ),
        migrations.AddField(
            model_name='ratting',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='ratting',
            unique_together={('user', 'movie')},
        ),
    ]