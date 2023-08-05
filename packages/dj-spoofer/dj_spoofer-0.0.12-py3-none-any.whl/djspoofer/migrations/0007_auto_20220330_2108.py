# Generated by Django 3.2.12 on 2022-03-30 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djspoofer', '0006_auto_20220330_1800'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='tlsfingerprint',
            name='tls_fp_client_index',
        ),
        migrations.RemoveField(
            model_name='fingerprint',
            name='tls_fingerprint',
        ),
        migrations.RemoveField(
            model_name='tlsfingerprint',
            name='client',
        ),
        migrations.AddField(
            model_name='tlsfingerprint',
            name='fingerprint',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, related_name='tls_fingerprint', to='djspoofer.fingerprint'),
            preserve_default=False,
        ),
    ]
