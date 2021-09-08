# Generated by Django 2.2.6 on 2020-07-27 01:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Administration', '0001_initial'),
        ('Education', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_document', models.BooleanField(default=False)),
                ('standard', models.IntegerField(default=0)),
                ('sender', models.CharField(max_length=40)),
                ('message', models.TextField(blank=True, max_length=500, null=True)),
                ('document', models.FileField(blank=True, max_length=500, null=True, upload_to='DataProcessorSystem/StaticDataProcessor/uploads/documents/')),
                ('sent_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('sent_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('message', models.TextField(max_length=600)),
                ('last_date', models.DateTimeField()),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_reminders', to='Education.Course')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('sent_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('message', models.TextField(max_length=600)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_notifications', to='Administration.Channel')),
                ('standard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='standard_notifications', to='Administration.Standard')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IndividualMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('sent_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('message', models.TextField(max_length=600)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channel_messages', to='Administration.Channel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('chats', models.ManyToManyField(blank=True, to='DashBoard.Chat')),
                ('standard', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='standard_groupchat', to='Administration.Standard')),
            ],
        ),
        migrations.CreateModel(
            name='Circular',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('sent_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('message', models.TextField(max_length=600)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_circulars', to='Administration.Department')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
