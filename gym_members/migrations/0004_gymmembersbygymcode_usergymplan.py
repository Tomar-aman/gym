# Generated by Django 5.1.4 on 2025-02-18 13:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_management', '0004_gymplan_duration'),
        ('gym_members', '0003_gymmembersbyowner_is_archive_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GymMembersByGymCode',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('is_archive', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='code_members', to='gym_management.gym')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gym_codes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserGymPlan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField()),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gym_memberships', to='gym_management.gym')),
                ('gym_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribed_users', to='gym_management.gymplan')),
                ('offline_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offline_memberships', to='gym_members.gymmembersbyowner')),
                ('online_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='online_memberships', to='gym_members.gymmembersbygymcode')),
            ],
        ),
    ]
