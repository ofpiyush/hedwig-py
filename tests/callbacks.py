__author__ = 'piyush'


def printer(ch, method, properties, body):
    print method.__dict__
    print properties.__dict__
    print body


def accounts_printer(ch, method, properties, body):
    print "Accounts printer called"
    printer(ch, method, properties, body)


def message_printer(ch, method, properties, body):
    print "Message printer called"
    printer(ch, method, properties, body)
