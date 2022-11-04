import socket
from parsers import parser
from constants import packet_formats, packet_ids
from packets import event, header

server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
server_socket.bind(('127.0.0.1', 20777))

saved_data = []

try:
  while(True):
    data, address = server_socket.recvfrom(2**16)
    parsed_header = parser.parse(data[0:header.LENGTH], header.PACKET)
    if parsed_header['packetId'] == packet_ids.EVENT:
      event_code = parser.parse(data[header.LENGTH:], event.PACKET)['eventStringCode']
      data_format = event.EVENT_MESSAGE_DATA[
        ''.join([x.decode('utf-8') for x in event_code])]
      if data_format is not None:
        packet = event.PACKET
        packet['eventDetails'] = data_format
        event_data = parser.parse(data[header.LENGTH:], packet)
      saved_data.append({
        'header': parsed_header,
        'data': event_data
      })
    else:
      saved_data.append({
        'header': parsed_header,
        'data': parser.parse(data[header.LENGTH:],
          packet_formats.PACKET_FORMATS[parsed_header['packetId']])
      })
except (KeyboardInterrupt, SystemExit) as exception:
  pass
