"""
Requisitos: python 3.6+, pandas

Enviar e-mail aos participantes, com o seu certificado em PDF
como anexo.

Arquivos locais e auxiliares, dentro de uma pasta chamada
"resource":
--------------------------------------------------------------------
* certificados/dados-emails.xlsx (planilha com os campos Nome, Sobrenome, Email
                 e Envio)
* oauthpyne.py (módulo Python onde são declaradas as variáveis de autenticação
                GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN)

* se mudar os nomes dos arquivos, ajuste o código em sndmail.py e mais abaixo,
    na criação do dataframe de participantes

*** Para configurar autenticação no GMail, veja o módulo sndmail.py

Arquivo de saída na pasta resource:
-----------------------------------
* email-certificado-enviado.xls (idêntico a dados-emails.xlsx com o registro no
    campo Envio ('S')

"""
import pandas as pd
import logging
from sndmail import send_mail

# configurar log
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# dicionario para tstes de envio
# participantes = [
#     {
#         'Nome': 'Fernando',
#         'Sobrenome': 'Júnior',
#         'Email': 'hildeberto@gmail.com',
#         'Envio': 'N'
#     },
#     {
#         'Nome': 'Hildeberto',
#         'Sobrenome': 'Magalhães',
#         'Email': 'hildeberto@gmail.com',
#         'Envio': 'N'
#     }
# ]

# dados gerais do e-mail
mail_from = 'nordeste@python.org.br'
assunto = '[Python Nordeste 2018] Certificado (pdf anexo)'
# dataframe com participantes
participantes = pd.read_excel('resource/certificados/dados-emails.xlsx')
# arquivo com registro de e-mails enviados
registro_envio = 'resource/certificados/email-certificado-enviado.xls'

# iteração sobre o dataframe de participantes
for indice, registro in participantes.iterrows():
    # se já houve envio anterior
    # próximo
    if registro['Envio'] == 'S':
        continue

    nome = registro['Nome']
    sobrenome = registro['Sobrenome']
    conteudo = f"""
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Python Nordeste 2018 - Certificado</title>
    </head>
    <body>
        <p>
            Olá <b>{nome} {sobrenome}</b>,
        </p>
        <p>
                Queremos lhe agradecer por ter estado conosco nesse 
            momento importante para a comunidade Python, que foi a Python 
            Nordeste 2018, na Paraíba. Segue em anexo seu Certificado de 
            Participação. Qualquer problema encontrado na confecção do 
            mesmo, favor nos contactar. 
                Lembramos a todos que a Python Brasil 2018 ocorrerá 
            em Natal, RN, de 17 a 22 de outubro. Nos encontramos lá?
        </p>
        <p>
            Abraços.
        </p>
        <p>
            PUG-PB (https://pb.python.org.br) <br />

            Python Nordeste 2018 <br />
            Site: https://2018.pythonnordeste.org <br />
            Twitter: twitter.com/pythonnordeste <br />
            Facebook: fb.com/PythonNordeste <br />
        </p>
    </body>
    </html>
    """
    mail_to = registro['Email']
    arquivo_certificado = (
        f'resource/certificados/certificado-'
        f'python-nordeste_Parte{indice+1}.pdf')

    # envio do email
    try:
        send_mail(mail_from, mail_to, assunto, conteudo, arquivo_certificado)
        participantes.loc[indice, 'Envio'] = 'S'
        logging.info(f'Certificado {arquivo_certificado} enviado para {nome} {sobrenome}.')
    except Exception as e:
        logging.error(f'Erro enviando para {nome} {sobrenome}: {mail_to}')
        logging.error(f'Notificação: {e}')
        pass

# registro do resultado final de envio de e-mails
try:
    participantes.to_excel(registro_envio)
    logging.info(f'Arquivo {registro_envio} salvo.')
except:
    logging.error(f'Problema ao salvar arquivo {registro_envio}.')
