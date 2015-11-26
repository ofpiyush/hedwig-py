# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BasicTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('char', models.CharField(max_length=255)),
                ('int', models.IntegerField()),
                ('nullable', models.CharField(max_length=255, null=True, blank=True)),
                ('date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ForeignKeyTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('char', models.CharField(max_length=255)),
                ('int', models.IntegerField()),
                ('nullable', models.CharField(max_length=255, null=True, blank=True)),
                ('date', models.DateTimeField()),
                ('basic', models.ForeignKey(to='chidiya.BasicTest')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HiddenTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('char', models.CharField(max_length=255)),
                ('int', models.IntegerField()),
                ('nullable', models.CharField(max_length=255, null=True, blank=True)),
                ('date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ManyToManyTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('char', models.CharField(max_length=255)),
                ('int', models.IntegerField()),
                ('nullable', models.CharField(max_length=255, null=True, blank=True)),
                ('date', models.DateTimeField()),
                ('uuid', models.UUIDField()),
                ('url', models.URLField()),
                ('basic', models.ManyToManyField(to='chidiya.BasicTest')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
