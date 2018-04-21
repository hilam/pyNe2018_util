"""
Requisitos: python 3.6+, pandas

Enviar e-mail aos palestrantes selecionados, comunicando data e hora da
palestra e solicitando confirmação, foto e bio para o site. Se o palestrante
ainda não se inscreveu, envia também um código de cupom para compra do
ingresso com desconto.

Arquivos locais e auxiliares, dentro de uma pasta chamada "resource":
---------------------------------------------------------------------
* programacao.xlsx (planilha com os campos Data, Hora, Local, Título,
                Palestrante, E-mail, Inscrito?, Confirmou? e Envio)
* oauthpyne.py (módulo Python onde são declaradas as variáveis de autenticação
                GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN)

* se mudar os nomes dos arquivos, ajuste o código em sndmail.py e mais abaixo,
    na criação do dataframe de palestras

*** Para configurar autenticação no GMail, veja o módulo sndmail.py

Arquivo de saída na pasta resource:
-----------------------------------
* programa-email-enviado.xls (idêntico a programação.xlsx com incremento do
    campo Envio

"""
import pandas as pd
import logging
from sndmail import send_mail

# configurar log
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
# dados gerais do e-mail
mail_from = 'nordeste@python.org.br'
assunto = '[Python Nordeste 2018] Sua palestra foi aceita!'
# dataframe com a programação
palestras = pd.read_excel('resource/programa.xlsx')
# arquivo com registro de e-mails enviados
registro_envio = 'resource/programa-email-enviado.xls'

# iteração sobre as palestras
for indice, registro in palestras.iterrows():
    # se já houve confirmação e o palestrante já se inscreveu, vai para o
    # próximo
    if registro['Confirmou?'] == 'S':
        if registro['Inscrito?'] == 'S':
            continue
    # dados para o texto do e-mail
    nome = registro['Palestrante']
    palestra = registro['Título']
    data = registro['Data'].strftime('%d/%m/%Y')
    hora = registro['Hora'].strftime('%H:%M')
    local = registro['Local']
    mail_to = registro['E-mail']
    inscrito = registro['Inscrito?']
    envio = registro['Envio']

    precisa_confirmar = ""
    if registro['Confirmou?'] == 'N':
        precisa_confirmar = """<p>
                Agora gostaríamos que nos confirmasse sua presença e 
            disponibilidade para o dia e horário proposto. <b>Caso haja o 
            aceite</b>, por gentileza <b>nos encaminhe uma foto e uma breve 
            apresentação sua</b>, com no máximo 200 caracteres, para colocarmos 
            em nosso site oficial.
        </p>"""

    desconto = ""
    if inscrito == 'N':
        desconto = """<p>
        Por fim, informamos que para participar do evento, mesmo como 
    palestrante, é necessário adquirir um ingresso. Com isso, criamos um código 
    promocional - <b>PALESTRANTE-PYNE2018</b> - que garante um desconto de R$ 
    20,00 no Lote Único - Inteira. Para mais informações sobre compra de 
    ingressos acesse o site https://2018.pythonnordeste.org
        </p>"""

    conteudo = f"""
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Python Nordeste 2018 - palestra selecionada</title>
    </head>
    <body>
        <p>
            Olá <b>{nome}</b>, tudo bem?
        </p>
        <p>
                Queremos lhe desejar os parabéns. Sua proposta <b>{palestra}</b> 
            foi selecionada e já está em nossa programação para o dia <b>{data}
            </b>, às <b>{hora}h</b>, na <b>{local}</b>, com duração de 30min 
            e 5min para perguntas.
        </p>
            {precisa_confirmar}
            {desconto}
        <p>
            Abraços.
        </p>
        <p>
            Fernando Júnior - PUG-PB <br />
            Python Nordeste 2018 <br />
            Site: https://2018.pythonnordeste.org <br />
            Twitter: twitter.com/pythonnordeste <br />
            Facebook: fb.com/PythonNordeste <br />
        </p>
    </body>
    </html>
    """

    # envio do email
    try:
        send_mail(mail_from, mail_to, assunto, conteudo)
        palestras.loc[indice, 'Envio'] += 1.0
        logging.info(f'Email enviado para {nome}.')
    except RuntimeError as e:
        logging.error(f'Erro enviando para {nome}: {mail_to}')
        logging.error(f'Notificação: {e}')
        pass

# registro do resultado final de envio de e-mails
try:
    palestras.to_excel(registro_envio)
    logging.info(f'Arquivo {registro_envio} salvo.')
except:
    logging.error(f'Problema ao salvar arquivo {registro_envio}.')

logging.info("Fim de processamento.")
