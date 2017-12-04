import googleapiclient.discovery


def entities_text(text):
    response = analyze_entities(text)
    return response


def analyze_entities(text, encoding='UTF32'):
    try:
        body = {
            'document': {
                'type': 'PLAIN_TEXT',
                'content': 'Name my ' + text,
            },
            'encoding_type': encoding,
        }

        service = googleapiclient.discovery.build('language', 'v1')

        request = service.documents().analyzeEntities(body=body)
        response = request.execute()

        entities = response['entities']
        subject = entities[-1]

        response = subject['type']

        dict = {'UNKNOWN': 'OTHER', 'PERSON': 'PERSON', 'LOCATION': 'PLACE', 'ORGANIZATION': 'ORGANIZATION',
                'EVENT': 'EVENT', 'WORK_OF_ART': 'WORK OF ART', 'CONSUMER_GOOD': 'CONSUMER GOOD', 'OTHER': 'OTHER'}

    except:
        return 'OTHER'
    else:
        return dict[response]
