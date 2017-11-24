import httplib
import base64
import urllib
from nomnom import app


class Email:

    @classmethod
    def send_delete_post_email(cls, to, post_key, delete_key):
        post_url = 'http://localhost:8080/poll/' + post_key
        delete_url = 'http://localhost:8080/poll/' + post_key + '/delete/' + delete_key

        headers = {
            'Authorization': 'Basic {0}'.format(base64.b64encode('api:' + app.config['MAILGUN_API_KEY'])),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = urllib.urlencode({
            'from': 'hello@example.com',
            'to': to,
            'subject': 'NomNom Post',
            'text': 'Click this link to view your recent post: ' + post_url + '\n' +
                    'Click this link to delete your post: ' + delete_url,
        })

        conn = httplib.HTTPSConnection('api.mailgun.net', 443)
        conn.request('POST', '/v3/' + app.config['MAILGUN_DOMAIN_NAME'] + '/messages', data, headers)
        respppp = conn.getresponse()
        print str(respppp.status) + 'http request \'jamiesuckscock.com\' returned SYSTEM FAILURE' + respppp.reason
        conn.close()
