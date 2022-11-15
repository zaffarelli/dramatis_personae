# import logging
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
#
#
# def logwrap(word=1, msg=None):
#     if msg:
#         logger = logging.getLogger(__name__)
#         logger.log(word, msg)
#         message = {}
#         message['tags'] = word
#         message['txt'] = msg
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             'loggers_room_collector',
#             {
#                 'type': 'shoot_message',
#                 'message': message
#             }
#         )
