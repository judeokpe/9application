# Generated by Django 4.2.4 on 2024-08-01 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('craeted', models.DateTimeField(auto_now_add=True)),
                ('user_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thread_user_one', to=settings.AUTH_USER_MODEL)),
                ('user_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thread_user_two', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('attached_file', models.FileField(blank=True, default=None, null=True, upload_to='attachments/%Y/%M/%d')),
                ('attached_file_name', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msgs_received', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msgs_sent', to=settings.AUTH_USER_MODEL)),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msgthread', to='chat.thread')),
            ],
            options={
                'ordering': ['-created'],
                'indexes': [models.Index(fields=['sender', 'receiver'], name='chat_chatme_sender__34ee69_idx'), models.Index(fields=['-created'], name='chat_chatme_created_c746bc_idx')],
            },
        ),
    ]
