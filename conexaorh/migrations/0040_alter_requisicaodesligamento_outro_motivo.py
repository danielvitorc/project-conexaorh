# Generated by Django 5.1.7 on 2025-05-27 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conexaorh', '0039_requisicaodesligamento_bloqueio_readmissao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisicaodesligamento',
            name='outro_motivo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
