# Generated by Django 3.2.12 on 2022-03-30 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djspoofer', '0005_auto_20220328_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='tlsfingerprint',
            name='client',
            field=models.IntegerField(choices=[(5, 'GENERIC'), (20, 'CHROME_DESKTOP'), (30, 'FIREFOX_DESKTOP')], default=5),
        ),
        migrations.AddIndex(
            model_name='tlsfingerprint',
            index=models.Index(fields=['client'], name='tls_fp_client_index'),
        ),
    ]
