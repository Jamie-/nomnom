import httplib
import base64
import urllib  # requests module not supported by GAE so using urllib instead
import logging
from nomnom import app

BASE_URL = 'http://localhost:8080/poll/'  # TODO Temporary URL

class Email:

    @classmethod
    def send_mail(cls, to, poll_id, delete_key):
        post_url = BASE_URL + poll_id
        delete_url = BASE_URL + poll_id + '/delete/' + delete_key

        headers = {
            'Authorization': 'Basic {0}'.format(base64.b64encode('api:' + app.config['MAILGUN_API_KEY'])),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = urllib.urlencode({
            'from': 'hello@nomnom.com',
            'to': to,
            'subject': 'New Poll Created - NomNom',
            'text': 'Click this link to view your recent post: ' + post_url + '\n' +
                    'Click this link to delete your post: ' + delete_url,
        })

        conn = httplib.HTTPSConnection('api.mailgun.net', 443)
        conn.request('POST', '/v3/{}/messages'.format(app.config['MAILGUN_DOMAIN_NAME']), data, headers)
        response = conn.getresponse()
        logging.debug('Attempting to send mail to "%s".', to)
        logging.debug('MailGun responded: %d %s\n%s', response.status, response.reason, response.read())
        conn.close()
