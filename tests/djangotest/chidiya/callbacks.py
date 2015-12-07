import json
from .models import HiddenTest


def printer(ch, method, properties, body):
    print "inside printer"
    print method.routing_key
    print body
    body_dict = json.loads(body)
    print body_dict
    if 'model' in body_dict and body_dict['model'] == "chidiya.basictest":
        print "Found model, will create hidden object"
        fields = body_dict['fields']
        fields.pop('id', None)
        HiddenTest.objects.create(**fields)
