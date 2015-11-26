__author__ = 'piyush'
import json


def printer(ch, method, properties, body):
    print method.routing_key
    print body
    body_dict = json.loads(body)
    if 'id' in body_dict and body_dict['id'] == 9998:
        raise Exception("kuch bhi")


def accounts_printer(ch, method, properties, body):
    print "Accounts printer called"
    printer(ch, method, properties, body)


def message_printer(ch, method, properties, body):
    print "Message printer called"
    printer(ch, method, properties, body)
