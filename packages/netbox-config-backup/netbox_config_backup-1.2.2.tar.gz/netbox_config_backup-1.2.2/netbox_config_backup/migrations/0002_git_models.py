# Generated by Django 3.2.8 on 2021-11-22 23:14

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('extras', '0062_clear_secrets_changelog'),
        ('netbox_config_backup', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackupCommit',
            fields=[
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sha', models.CharField(max_length=64)),
                ('backup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='netbox_config_backup.backup')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='backupjob',
            name='backup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='netbox_config_backup.backup'),
        ),
        migrations.CreateModel(
            name='BackupObject',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sha', models.CharField(max_length=64)),
                ('file', models.CharField(max_length=255)),
            ],
            options={
                'unique_together': {('sha', 'file')},
            },
        ),
        migrations.CreateModel(
            name='BackupCommitTreeChange',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=10)),
                ('commit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='changes', to='netbox_config_backup.backupcommit')),
                ('new', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='new', to='netbox_config_backup.backupobject')),
                ('old', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='previous', to='netbox_config_backup.backupobject')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
