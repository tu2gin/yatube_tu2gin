# Generated by Django 2.2.9 on 2021-11-03 12:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20211103_1503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='group_id',
        ),
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.Group'),
        ),
    ]
