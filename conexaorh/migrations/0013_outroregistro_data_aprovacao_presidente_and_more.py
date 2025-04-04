# Generated by Django 5.1.7 on 2025-04-02 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conexaorh', '0012_outroregistro_data_aprovacao_diretor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='outroregistro',
            name='data_aprovacao_presidente',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='outroregistro',
            name='dias_para_aprovacao_presidente',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='outroregistro',
            name='status_presidente',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('aprovado', 'Aprovado'), ('rejeitado', 'Rejeitado')], default='pendente', max_length=20),
        ),
    ]
