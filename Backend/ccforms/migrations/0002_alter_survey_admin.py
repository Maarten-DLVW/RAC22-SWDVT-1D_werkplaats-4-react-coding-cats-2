# Generated by Django 4.0.10 on 2023-06-03 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ccforms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ccforms.administrator', verbose_name='Administrator'),
        ),
    ]
