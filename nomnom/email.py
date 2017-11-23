import requests

MAILGUN_DOMAIN_NAME = "sandboxc753467df1ae49bea3687991b980ba6b.mailgun.org"
MAILGUN_API_KEY = "key-dbdf2012d4409df162546794dc8a66a1"


class Email:

    def __init__(self):
        pass

    @classmethod
    def send_delete_post_email(cls, to, post_key, delete_key):
        url = 'https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN_NAME)
        auth = ('api', MAILGUN_API_KEY)
        data = {
            'from': 'NomNom <mailgun@{}>'.format(MAILGUN_DOMAIN_NAME),
            'to': to,
            'subject': 'NomNom Post',
            'text': 'Click this link to view your recent post: ' + post_key + '\n' +  # todo make into link
                    'Click this link to delete your post: ' + delete_key,  # todo make into link
        }

        response = requests.post(url, auth=auth, data=data)
        response.raise_for_status()

        return

# You can see a record of this email in your logs: https://mailgun.com/app/logs .
# You can send up to 300 emails/day from this sandbox server.
# Next, you should add your own domain so you can send 10,000 emails/month for free.
