# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FaculdadeNegociosFan(models.Model):
    email = models.TextField(db_column='Email', blank=True, null=True)  # Field name made lowercase.
    nome = models.TextField(db_column='Nome', blank=True, null=True)  # Field name made lowercase.
    telefone = models.TextField(db_column='Telefone', blank=True, null=True)  # Field name made lowercase.
    celular = models.TextField(db_column='Celular', blank=True, null=True)  # Field name made lowercase.
    cargo = models.TextField(db_column='Cargo', blank=True, null=True)  # Field name made lowercase.
    estado = models.TextField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.
    cidade = models.TextField(db_column='Cidade', blank=True, null=True)  # Field name made lowercase.
    estagio_no_funil = models.TextField(db_column='Estagio no funil', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_da_ultima_oportunidade = models.DateField(db_column='Data da ultima oportunidade', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_da_ultima_venda = models.DateField(db_column='Data da ultima venda', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_da_primeira_conversao = models.DateField(db_column='Data da primeira conversao', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    origem_da_primeira_conversao = models.TextField(db_column='Origem da primeira conversao', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_da_ultima_conversao = models.DateField(db_column='Data da ultima conversao', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    origem_da_ultima_conversao = models.TextField(db_column='Origem da ultima conversao', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    formacao = models.TextField(db_column='Formacao', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'faculdade_negocios_fan'


class FaculdadeNegociosFanConversions(models.Model):
    page_id = models.IntegerField()
    page_name = models.CharField(max_length=100, blank=True, null=True)
    conversion = models.IntegerField()
    date = models.DateField()
    page_url = models.CharField(max_length=54, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculdade_negocios_fan_conversions'


class FaculdadeNegociosFanEmails(models.Model):
    date = models.DateField(blank=True, null=True)
    identificador = models.BigIntegerField(db_column='Identificador', blank=True, null=True)  # Field name made lowercase.
    data_de_envio_dd_mm_aaaa_field = models.DateField(db_column='Data de envio (dd/mm/aaaa)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    dia_da_semana = models.TextField(db_column='Dia da semana', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nome_do_email = models.TextField(db_column='Nome do email', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    assunto = models.TextField(db_column='Assunto', blank=True, null=True)  # Field name made lowercase.
    leads_selecionados = models.IntegerField(db_column='Leads selecionados', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descartados = models.IntegerField(db_column='Descartados', blank=True, null=True)  # Field name made lowercase.
    entregues = models.IntegerField(db_column='Entregues', blank=True, null=True)  # Field name made lowercase.
    bounce_unicos_field = models.IntegerField(db_column='Bounce (unicos)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    aberturas_unicas_field = models.IntegerField(db_column='Aberturas (unicas)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    cliques_unicos_field = models.IntegerField(db_column='Cliques (unicos)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    descadastrados = models.IntegerField(db_column='Descadastrados', blank=True, null=True)  # Field name made lowercase.
    marcados_como_spam = models.IntegerField(db_column='Marcados como spam', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tipo_de_email = models.TextField(db_column='Tipo de email', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    status_do_email = models.TextField(db_column='Status do email', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nome_do_remetente = models.TextField(db_column='Nome do remetente', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    email_do_remetente = models.TextField(db_column='Email do remetente', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    segmentacoes_de_envio = models.TextField(db_column='Segmentacoes de envio', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    segmentacoes_excluidas = models.TextField(db_column='Segmentacoes excluidas', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niveis_de_engajamento_leads_engajados = models.TextField(db_column='Niveis de engajamento - Leads engajados', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niveis_de_engajamento_leads_desengajados = models.TextField(db_column='Niveis de engajamento - Leads desengajados', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niveis_de_engajamento_leads_indeterminados = models.TextField(db_column='Niveis de engajamento - Leads indeterminados', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'faculdade_negocios_fan_emails'


class Pointer(models.Model):
    email = models.CharField(db_column='Email', primary_key=True, max_length=64)  # Field name made lowercase.
    nome = models.TextField(db_column='Nome', blank=True, null=True)  # Field name made lowercase.
    telefone = models.TextField(db_column='Telefone', blank=True, null=True)  # Field name made lowercase.
    celular = models.TextField(db_column='Celular', blank=True, null=True)  # Field name made lowercase.
    cargo = models.TextField(db_column='Cargo', blank=True, null=True)  # Field name made lowercase.
    estado = models.TextField(db_column='Estado', blank=True, null=True)  # Field name made lowercase.
    cidade = models.TextField(db_column='Cidade', blank=True, null=True)  # Field name made lowercase.
    estagio_no_funil = models.TextField(db_column='Estagio no funil', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_da_ultima_oportunidade = models.DateField(db_column='Data da ultima oportunidade', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_da_ultima_venda = models.DateField(db_column='Data da ultima venda', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_da_primeira_conversao = models.DateField(db_column='Data da primeira conversao', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    origem_da_primeira_conversao = models.TextField(db_column='Origem da primeira conversao', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_da_ultima_conversao = models.DateField(db_column='Data da ultima conversao', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    origem_da_ultima_conversao = models.TextField(db_column='Origem da ultima conversao', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cnpj = models.TextField(db_column='CNPJ', blank=True, null=True)  # Field name made lowercase.
    empresa = models.TextField(db_column='Empresa', blank=True, null=True)  # Field name made lowercase.
    cuttly_link = models.CharField(max_length=25, blank=True, null=True)
    loja = models.TextField(db_column='Loja', blank=True, null=True)  # Field name made lowercase.
    qr_email_sent = models.IntegerField(blank=True, null=True)
    event_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pointer'


class Previda(models.Model):
    email = models.CharField(db_column='Email', max_length=41, blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=42, blank=True, null=True)  # Field name made lowercase.
    telefone = models.CharField(db_column='Telefone', max_length=19, blank=True, null=True)  # Field name made lowercase.
    celular = models.CharField(db_column='Celular', max_length=10, blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cidade = models.CharField(db_column='Cidade', max_length=10, blank=True, null=True)  # Field name made lowercase.
    data = models.DateField(db_column='Data', blank=True, null=True)  # Field name made lowercase.
    origem_da_primeira_conversão = models.CharField(db_column='Origem da primeira conversão', max_length=49, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'previda'


class PrevidaConversions(models.Model):
    page_id = models.IntegerField()
    page_name = models.CharField(max_length=100, blank=True, null=True)
    conversion = models.IntegerField()
    date = models.DateField()
    page_url = models.CharField(max_length=54, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'previda_conversions'


class PrevidaEmails(models.Model):
    date = models.DateField(blank=True, null=True)
    identificador = models.BigIntegerField(db_column='Identificador', blank=True, null=True)  # Field name made lowercase.
    data_de_envio_dd_mm_aaaa_field = models.DateField(db_column='Data de envio (dd/mm/aaaa)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    dia_da_semana = models.TextField(db_column='Dia da semana', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nome_do_email = models.TextField(db_column='Nome do email', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    assunto = models.TextField(db_column='Assunto', blank=True, null=True)  # Field name made lowercase.
    leads_selecionados = models.IntegerField(db_column='Leads selecionados', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descartados = models.IntegerField(db_column='Descartados', blank=True, null=True)  # Field name made lowercase.
    entregues = models.IntegerField(db_column='Entregues', blank=True, null=True)  # Field name made lowercase.
    bounce_unicos_field = models.IntegerField(db_column='Bounce (unicos)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    aberturas_unicas_field = models.IntegerField(db_column='Aberturas (unicas)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    cliques_unicos_field = models.IntegerField(db_column='Cliques (unicos)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    descadastrados = models.IntegerField(db_column='Descadastrados', blank=True, null=True)  # Field name made lowercase.
    marcados_como_spam = models.IntegerField(db_column='Marcados como spam', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tipo_de_email = models.TextField(db_column='Tipo de email', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    status_do_email = models.TextField(db_column='Status do email', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nome_do_remetente = models.TextField(db_column='Nome do remetente', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    email_do_remetente = models.TextField(db_column='Email do remetente', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    segmentacoes_de_envio = models.TextField(db_column='Segmentacoes de envio', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    segmentacoes_excluidas = models.TextField(db_column='Segmentacoes excluidas', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niveis_de_engajamento_leads_engajados = models.TextField(db_column='Niveis de engajamento - Leads engajados', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niveis_de_engajamento_leads_desengajados = models.TextField(db_column='Niveis de engajamento - Leads desengajados', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niveis_de_engajamento_leads_indeterminados = models.TextField(db_column='Niveis de engajamento - Leads indeterminados', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'previda_emails'


class SebraeAl(models.Model):
    email = models.CharField(db_column='Email', max_length=41, blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=42, blank=True, null=True)  # Field name made lowercase.
    telefone = models.CharField(db_column='Telefone', max_length=19, blank=True, null=True)  # Field name made lowercase.
    celular = models.CharField(db_column='Celular', max_length=10, blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cidade = models.CharField(db_column='Cidade', max_length=10, blank=True, null=True)  # Field name made lowercase.
    data = models.DateField(db_column='Data', blank=True, null=True)  # Field name made lowercase.
    origem_da_primeira_conversão = models.CharField(db_column='Origem da primeira conversão', max_length=49, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cnpj = models.CharField(db_column='CNPJ', max_length=25, blank=True, null=True)  # Field name made lowercase.
    cpf = models.CharField(db_column='CPF', max_length=15, blank=True, null=True)  # Field name made lowercase.
    tipo_de_empresa = models.CharField(db_column='Tipo de empresa', max_length=10, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'sebrae_al'


class SebraeAlConversions(models.Model):
    page_id = models.IntegerField()
    page_name = models.CharField(max_length=100, blank=True, null=True)
    conversion = models.IntegerField()
    date = models.DateField()
    page_url = models.CharField(max_length=54, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sebrae_al_conversions'


class SebraeAlEmails(models.Model):
    date = models.DateField(blank=True, null=True)
    identificador = models.BigIntegerField(db_column='Identificador', blank=True, null=True)  # Field name made lowercase.
    data_de_envio_dd_mm_aaaa_field = models.DateField(db_column='Data de envio (dd/mm/aaaa)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    dia_da_semana = models.TextField(db_column='Dia da semana', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nome_do_email = models.TextField(db_column='Nome do email', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    assunto = models.TextField(db_column='Assunto', blank=True, null=True)  # Field name made lowercase.
    leads_selecionados = models.IntegerField(db_column='Leads selecionados', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descartados = models.IntegerField(db_column='Descartados', blank=True, null=True)  # Field name made lowercase.
    entregues = models.IntegerField(db_column='Entregues', blank=True, null=True)  # Field name made lowercase.
    bounce_unicos_field = models.IntegerField(db_column='Bounce (unicos)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    aberturas_unicas_field = models.IntegerField(db_column='Aberturas (unicas)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    cliques_unicos_field = models.IntegerField(db_column='Cliques (unicos)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    descadastrados = models.IntegerField(db_column='Descadastrados', blank=True, null=True)  # Field name made lowercase.
    marcados_como_spam = models.IntegerField(db_column='Marcados como spam', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tipo_de_email = models.TextField(db_column='Tipo de email', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    status_do_email = models.TextField(db_column='Status do email', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nome_do_remetente = models.TextField(db_column='Nome do remetente', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    email_do_remetente = models.TextField(db_column='Email do remetente', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    segmentacoes_de_envio = models.TextField(db_column='Segmentacoes de envio', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    segmentacoes_excluidas = models.TextField(db_column='Segmentacoes excluidas', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niveis_de_engajamento_leads_engajados = models.TextField(db_column='Niveis de engajamento - Leads engajados', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niveis_de_engajamento_leads_desengajados = models.TextField(db_column='Niveis de engajamento - Leads desengajados', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niveis_de_engajamento_leads_indeterminados = models.TextField(db_column='Niveis de engajamento - Leads indeterminados', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'sebrae_al_emails'


class Splitsecond(models.Model):
    email = models.CharField(db_column='Email', max_length=41, blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=42, blank=True, null=True)  # Field name made lowercase.
    telefone = models.CharField(db_column='Telefone', max_length=19, blank=True, null=True)  # Field name made lowercase.
    celular = models.CharField(db_column='Celular', max_length=10, blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cidade = models.CharField(db_column='Cidade', max_length=10, blank=True, null=True)  # Field name made lowercase.
    data = models.DateField(db_column='Data', blank=True, null=True)  # Field name made lowercase.
    origem_da_primeira_conversão = models.CharField(db_column='Origem da primeira conversão', max_length=49, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'splitsecond'


class SplitsecondConversions(models.Model):
    page_id = models.IntegerField()
    page_name = models.CharField(max_length=100, blank=True, null=True)
    conversion = models.IntegerField()
    date = models.DateField()
    page_url = models.CharField(max_length=54, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'splitsecond_conversions'


class SplitsecondEmails(models.Model):
    date = models.DateField(blank=True, null=True)
    identificador = models.BigIntegerField(db_column='Identificador', blank=True, null=True)  # Field name made lowercase.
    data_de_envio_dd_mm_aaaa_field = models.DateField(db_column='Data de envio (dd/mm/aaaa)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    dia_da_semana = models.TextField(db_column='Dia da semana', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nome_do_email = models.TextField(db_column='Nome do email', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    assunto = models.TextField(db_column='Assunto', blank=True, null=True)  # Field name made lowercase.
    leads_selecionados = models.IntegerField(db_column='Leads selecionados', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    descartados = models.IntegerField(db_column='Descartados', blank=True, null=True)  # Field name made lowercase.
    entregues = models.IntegerField(db_column='Entregues', blank=True, null=True)  # Field name made lowercase.
    bounce_unicos_field = models.IntegerField(db_column='Bounce (unicos)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    aberturas_unicas_field = models.IntegerField(db_column='Aberturas (unicas)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    cliques_unicos_field = models.IntegerField(db_column='Cliques (unicos)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    descadastrados = models.IntegerField(db_column='Descadastrados', blank=True, null=True)  # Field name made lowercase.
    marcados_como_spam = models.IntegerField(db_column='Marcados como spam', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tipo_de_email = models.TextField(db_column='Tipo de email', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    status_do_email = models.TextField(db_column='Status do email', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nome_do_remetente = models.TextField(db_column='Nome do remetente', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    email_do_remetente = models.TextField(db_column='Email do remetente', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    segmentacoes_de_envio = models.TextField(db_column='Segmentacoes de envio', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    segmentacoes_excluidas = models.TextField(db_column='Segmentacoes excluidas', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niveis_de_engajamento_leads_engajados = models.TextField(db_column='Niveis de engajamento - Leads engajados', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niveis_de_engajamento_leads_desengajados = models.TextField(db_column='Niveis de engajamento - Leads desengajados', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    niveis_de_engajamento_leads_indeterminados = models.TextField(db_column='Niveis de engajamento - Leads indeterminados', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'splitsecond_emails'
