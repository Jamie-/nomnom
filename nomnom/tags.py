import googleapiclient.discovery


def entities_text(text):
    response = analyze_entities(text)
    return response


# check for search terms and sort orders for the url presented in the tag selection drop down
def gen_tag_url(request):
    if request.path == '/search':
        tag_url = request.path + '?'
    else:
        tag_url = "/?"
    if "q" in request.args:
        tag_url = tag_url + "q=" + request.args.get("q") + "&"
    if "order" in request.args:
        tag_url = tag_url + "order=" + request.args.get("order") + "&"
    return tag_url


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
