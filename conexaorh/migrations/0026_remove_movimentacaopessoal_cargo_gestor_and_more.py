# Generated by Django 5.1.7 on 2025-04-07 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conexaorh', '0025_alter_requisicaodesligamento_centro_custo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movimentacaopessoal',
            name='cargo_gestor',
        ),
        migrations.RemoveField(
            model_name='movimentacaopessoal',
            name='descricao',
        ),
        migrations.RemoveField(
            model_name='movimentacaopessoal',
            name='nome_gestor',
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='cargo_atual',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='cargo_proposto',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='centro_custo_atual',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='centro_custo_proposto',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='colaborador_movimentado',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='comentarios',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='data_admissao',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='data_movimentacao',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='departamento_atual',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='departamento_proposto',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='gestor_atual',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='gestor_proposto',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='jutificativa_movimentacao',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='localidade_atual',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='localidade_proposta',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='matricula',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='numero',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='outro_info',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='outro_justificativa',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='outro_tipo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='periodo',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='salario_atual',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='salario_proposto',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='substituicao',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='tipo_adicional',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='tipo_ajuda_custo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='tipo_movimentacao',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='unidade',
            field=models.CharField(blank=True, default='MANAUS', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movimentacaopessoal',
            name='valor_ajuda',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movimentacaopessoal',
            name='data_solicitacao',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
