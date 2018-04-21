"""
Módulo para envio de e-mail utilizando o SMTP do GMail com autenticação OAuth

Ler o artigo e seguir as instruções da parte manual:
# http://blog.macuyiko.com/post/2016/how-to-send-html-mails-with-oauth2-and-gmail-in-python.html

Adapted from:
https://github.com/google/gmail-oauth2-tools/blob/master/python/oauth2.py
https://developers.google.com/identity/protocols/OAuth2

1. Generate and authorize an OAuth2 (generate_oauth2_token)
2. Generate a new access tokens using a refresh token(refresh_token)
3. Generate an OAuth2 string to use for login (access_token)

"""
import base64
import imaplib
import json
import smtplib
import urllib.parse
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import lxml.html
# Elementos para autenticação OAuth devem ser colocadas no arquivo
# resource/oauthpyne.py.
from resource.oauthpyne import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, \
    GOOGLE_REFRESH_TOKEN

# Quando necessitar de um TOKEN válido (no primeiro uso da autenticação ou
# quando EXPIRAR o token), execute este módulo com a linha seguinte ativada:
# GOOGLE_REFRESH_TOKEN = None

GOOGLE_ACCOUNTS_BASE_URL = 'https://accounts.google.com'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'


def command_to_url(command):
    return '%s/%s' % (GOOGLE_ACCOUNTS_BASE_URL, command)


def url_escape(text):
    return urllib.parse.quote(text, safe='~-._')


def url_unescape(text):
    return urllib.parse.unquote(text)


def url_format_params(params):
    param_fragments = []
    for param in sorted(params.items(), key=lambda x: x[0]):
        param_fragments.append('%s=%s' % (param[0], url_escape(param[1])))
    return '&'.join(param_fragments)


def generate_permission_url(client_id, scope='https://mail.google.com/'):
    params = {'client_id': client_id, 'redirect_uri': REDIRECT_URI,
              'scope': scope, 'response_type': 'code'}
    return '%s?%s' % (command_to_url('o/oauth2/auth'),
                      url_format_params(params))


def call_authorize_tokens(client_id, client_secret, authorization_code):
    params = {'client_id': client_id, 'client_secret': client_secret,
              'code': authorization_code, 'redirect_uri': REDIRECT_URI,
              'grant_type': 'authorization_code'}
    request_url = command_to_url('o/oauth2/token')
    response = urllib.request.urlopen(request_url, urllib.parse.urlencode(
        params).encode('UTF-8')).read().decode('UTF-8')
    return json.loads(response)


def call_refresh_token(client_id, client_secret, refresh_token):
    params = {'client_id': client_id, 'client_secret': client_secret,
              'refresh_token': refresh_token, 'grant_type': 'refresh_token'}
    request_url = command_to_url('o/oauth2/token')
    response = urllib.request.urlopen(request_url, urllib.parse.urlencode(
        params).encode('UTF-8')).read().decode('UTF-8')
    return json.loads(response)


def generate_oauth2_string(username, access_token, as_base64=False):
    auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
    if as_base64:
        auth_string = base64.b64encode(auth_string.encode(
            'ascii')).decode('ascii')
    return auth_string


def test_imap(user, auth_string):
    imap_conn = imaplib.IMAP4_SSL('imap.gmail.com')
    imap_conn.debug = 4
    imap_conn.authenticate('XOAUTH2', lambda x: auth_string)
    imap_conn.select('INBOX')


def test_smpt(user, base64_auth_string):
    smtp_conn = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_conn.set_debuglevel(True)
    smtp_conn.ehlo('test')
    smtp_conn.starttls()
    smtp_conn.docmd('AUTH', 'XOAUTH2 ' + base64_auth_string)


def get_authorization(google_client_id, google_client_secret):
    scope = "https://mail.google.com/"
    print('Abra um navegador e cole a seguinte URL:', generate_permission_url(
        google_client_id, scope))
    authorization_code = input('Entre com o código de verigicação '
                               'gerado no navegador: ')
    response = call_authorize_tokens(google_client_id, google_client_secret,
                                     authorization_code)
    return response['refresh_token'], response['access_token'], \
        response['expires_in']


def refresh_authorization(google_client_id, google_client_secret,
                          refresh_token):
    response = call_refresh_token(google_client_id, google_client_secret,
                                  refresh_token)
    return response['access_token'], response['expires_in']


def send_mail(fromaddr, toaddr, subject, message):
    access_token, expires_in = refresh_authorization(GOOGLE_CLIENT_ID,
                                                     GOOGLE_CLIENT_SECRET,
                                                     GOOGLE_REFRESH_TOKEN)
    auth_string = generate_oauth2_string(fromaddr, access_token, as_base64=True)

    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg.preamble = 'This is a multi-part message in MIME format.'
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    part_text = MIMEText(lxml.html.fromstring(
        message).text_content().encode('utf-8'), 'plain', _charset='utf-8')
    part_html = MIMEText(message.encode('utf-8'), 'html', _charset='utf-8')
    msg_alternative.attach(part_text)
    msg_alternative.attach(part_html)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo(GOOGLE_CLIENT_ID)
    server.starttls()
    server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()


if __name__ == '__main__':
    # Elements for authentication are in resource/oauthpyne.py
    if GOOGLE_REFRESH_TOKEN is None:
        print('TOKEN não encontrado. Obtendo um: ')
        refresh_token, access_token, expires_in = get_authorization(
            GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
        print('Configure o seu GOOGLE_REFRESH_TOKEN para o seguinte:',
              refresh_token)
        exit()

    send_mail('nordeste@python.org.br', 'nordeste@python.org.br',
              '[Python Nordeste 2018] Sua palestra foi aceita!',
              'Teatando autenticação')
