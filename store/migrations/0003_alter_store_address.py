# Generated by Django 4.1 on 2022-08-17 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_store_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='store', to='store.address'),
        ),
    ]
