# Generated by Django 5.1.7 on 2025-04-03 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conexaorh', '0014_outroregistro_data_aprovacao_rh_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='outroregistro',
            name='dias_para_aprovacao_diretor',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
