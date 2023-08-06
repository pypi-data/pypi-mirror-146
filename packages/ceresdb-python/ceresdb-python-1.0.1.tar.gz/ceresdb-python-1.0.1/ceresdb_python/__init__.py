import socket
import json
from typing import List, Dict
import time

PACKET_SIZE=65536
DATA_TERMINATOR='EOD'
ENCODING='utf-8'
__version__ = '1.0.1'

class Connection:
    def __init__(self, username: str, password: str, host: str, port: int) -> None:
        self.username = username
        self.password = password
        self.host = host
        self.port = port

    def query(self, query_string: str) -> List[Dict]:
        payload = {
            "_auth": f"{self.username}:{self.password}",
            "query": query_string
        }

        # Create the connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))

        # Send the query to the server
        s.sendall((json.dumps(payload)+'\n').encode(ENCODING))

        output_string = ''
        output_data = []

        # Grab the initial packet
        data = s.recv(PACKET_SIZE)
        if not data:
            raise Exception("The server closed the connection unexpectedly")

        # Grab any other packets if there's more data
        output_string += data.decode(ENCODING)
        while not data.decode(ENCODING).endswith(DATA_TERMINATOR):
            data = s.recv(PACKET_SIZE)
            output_string += data.decode(ENCODING)

        # Close the connection
        s.close()

        # Trim off terminator
        output_string = output_string[:-len(DATA_TERMINATOR)]

        # Process output that is returned
        if output_string != 'null':
            parsed = json.loads(output_string)
            if type(parsed) == dict:
                if 'error' in parsed.keys():
                    raise Exception(f"The server returned an error: {parsed['error']}")
            output_data = json.loads(output_string)

        return output_data

    def timed_query(self, query_string: str) -> tuple[List[Dict], Dict]:
        payload = {
            "_auth": f"{self.username}:{self.password}",
            "query": query_string
        }

        # Create the connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))

        # Send the query to the server
        send_start = time.time()
        s.sendall((json.dumps(payload)+'\n').encode(ENCODING))
        send_end = time.time()

        output_string = ''
        output_data = []

        # Grab the initial packet
        data = s.recv(PACKET_SIZE)
        receive_start = time.time()
        if not data:
            raise Exception("The server closed the connection unexpectedly")

        # Grab any other packets if there's more data
        output_string += data.decode(ENCODING)
        while not data.decode(ENCODING).endswith(DATA_TERMINATOR):
            data = s.recv(PACKET_SIZE)
            output_string += data.decode(ENCODING)
        receive_end = time.time()

        # Close the connection
        s.close()

        # Trim off terminator
        output_string = output_string[:-len(DATA_TERMINATOR)]

        # Process output that is returned
        if output_string != 'null':
            parsed = json.loads(output_string)
            if type(parsed) == dict:
                if 'error' in parsed.keys():
                    raise Exception(f"The server returned an error: {parsed['error']}")
            output_data = json.loads(output_string)

        timing = {
            "send": str(send_end - send_start),
            "process": str(receive_start - send_end),
            "receive": str(receive_end - receive_start)
        }

        return (output_data, timing)
