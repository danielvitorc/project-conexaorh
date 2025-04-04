# Generated by Django 5.1.7 on 2025-04-04 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conexaorh', '0020_requisicaodesligamento'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movimentacaopessoal',
            old_name='data_aprovacao_diretor',
            new_name='data_autorizacao_diretor',
        ),
        migrations.RenameField(
            model_name='movimentacaopessoal',
            old_name='data_aprovacao_presidente',
            new_name='data_autorizacao_presidente',
        ),
        migrations.RenameField(
            model_name='movimentacaopessoal',
            old_name='data_aprovacao_rh',
            new_name='data_autorizacao_rh',
        ),
        migrations.RenameField(
            model_name='movimentacaopessoal',
            old_name='data_criacao',
            new_name='data_solicitacao',
        ),
        migrations.RenameField(
            model_name='movimentacaopessoal',
            old_name='dias_para_aprovacao_diretor',
            new_name='dias_para_autorizacao_diretor',
        ),
        migrations.RenameField(
            model_name='movimentacaopessoal',
            old_name='dias_para_aprovacao_presidente',
            new_name='dias_para_autorizacao_presidente',
        ),
        migrations.RenameField(
            model_name='movimentacaopessoal',
            old_name='dias_para_aprovacao_rh',
            new_name='dias_para_autorizacao_rh',
        ),
        migrations.RenameField(
            model_name='requisicaodesligamento',
            old_name='data_aprovacao_diretor',
            new_name='data_autorizacao_diretor',
        ),
        migrations.RenameField(
            model_name='requisicaodesligamento',
            old_name='data_aprovacao_presidente',
            new_name='data_autorizacao_presidente',
        ),
        migrations.RenameField(
            model_name='requisicaodesligamento',
            old_name='data_aprovacao_rh',
            new_name='data_autorizacao_rh',
        ),
        migrations.RenameField(
            model_name='requisicaodesligamento',
            old_name='data_criacao',
            new_name='data_solicitacao',
        ),
        migrations.RenameField(
            model_name='requisicaodesligamento',
            old_name='dias_para_aprovacao_diretor',
            new_name='dias_para_autorizacao_diretor',
        ),
        migrations.RenameField(
            model_name='requisicaodesligamento',
            old_name='dias_para_aprovacao_presidente',
            new_name='dias_para_autorizacao_presidente',
        ),
        migrations.RenameField(
            model_name='requisicaodesligamento',
            old_name='dias_para_aprovacao_rh',
            new_name='dias_para_autorizacao_rh',
        ),
        migrations.RenameField(
            model_name='requisicaopessoal',
            old_name='data_aprovacao_diretor',
            new_name='data_autorizacao_diretor',
        ),
        migrations.RenameField(
            model_name='requisicaopessoal',
            old_name='data_aprovacao_presidente',
            new_name='data_autorizacao_presidente',
        ),
        migrations.RenameField(
            model_name='requisicaopessoal',
            old_name='data_aprovacao_rh',
            new_name='data_autorizacao_rh',
        ),
        migrations.RenameField(
            model_name='requisicaopessoal',
            old_name='data_criacao',
            new_name='data_solicitacao',
        ),
        migrations.RenameField(
            model_name='requisicaopessoal',
            old_name='dias_para_aprovacao_diretor',
            new_name='dias_para_autorizacao_diretor',
        ),
        migrations.RenameField(
            model_name='requisicaopessoal',
            old_name='dias_para_aprovacao_presidente',
            new_name='dias_para_autorizacao_presidente',
        ),
        migrations.RenameField(
            model_name='requisicaopessoal',
            old_name='dias_para_aprovacao_rh',
            new_name='dias_para_autorizacao_rh',
        ),
    ]
