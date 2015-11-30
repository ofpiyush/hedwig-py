from .settings import hedwig_settings
from hedwig.core.emitter import Emitter
import json

hedwig_emitter = Emitter(hedwig_settings)

# hedwig_emitter.emit('accounts.model.create.1', json.dumps({
#     'id': 1,
#     'username': 'piyush'
# }))
#
# hedwig_emitter.emit('message.serializer.create.asdf123', json.dumps({
#     'mid': "asdf123",
#     'from': 'piyush',
#     'to': 'sandeep',
#     'message': 'ye lo babua chal pada'
# }))

for x in range(1, 10000):
    hedwig_emitter.emit('accounts.model.create.{0}'.format(x), json.dumps({

        'id': x,
        'username': 'piyush'
    }))
