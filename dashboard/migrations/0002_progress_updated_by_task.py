# Generated by Django 5.2 on 2025-05-20 20:18

import django.db.models.deletion
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='progress',
            name='updated_by',
            field=models.CharField(default='', max_length=70),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('taskID', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=6)),
                ('text', django_ckeditor_5.fields.CKEditor5Field()),
                ('date', models.DateField(auto_now_add=True)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('assignedTo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_given_to', to='dashboard.volunteer')),
            ],
        ),
    ]
