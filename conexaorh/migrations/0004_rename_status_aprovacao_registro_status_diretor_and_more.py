# Generated by Django 5.1.7 on 2025-04-02 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conexaorh', '0003_registro_status_aprovacao'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registro',
            old_name='status_aprovacao',
            new_name='status_diretor',
        ),
        migrations.AddField(
            model_name='registro',
            name='status_presidente',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('aprovado', 'Aprovado'), ('rejeitado', 'Rejeitado')], default='pendente', max_length=20),
        ),
    ]
