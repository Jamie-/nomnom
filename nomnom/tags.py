import googleapiclient.discovery

# analyses text to return a single category as a string
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

        # requests JSON response from API
        request = service.documents().analyzeEntities(body=body)
        response = request.execute()

        # selects the last entity to be mentioned in the title as the subject
        subject = response['entities'][-1]

        # gets the type of the subject
        tag = subject['type']

        # API entity types to human readable tags.
        dict = {'UNKNOWN': 'OTHER', 'PERSON': 'PERSON', 'LOCATION': 'PLACE', 'ORGANIZATION': 'ORGANIZATION',
                'EVENT': 'EVENT', 'WORK_OF_ART': 'WORK OF ART', 'CONSUMER_GOOD': 'CONSUMER GOOD', 'OTHER': 'OTHER'}

    except:
        return 'OTHER'
    else:
        return dict[tag]
