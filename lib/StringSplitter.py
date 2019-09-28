from string import *
import zlib
import json
from math import ceil
from base64 import b64encode, b64decode
import textwrap


class StringSplitter:
    _input_string = None
    _number_of_databases = None
    _number_of_chunks = None
    _chunk_length = None
    _chunks = None

    def __init__(self, input_string, number_of_databases):
        self._input_string = input_string
        if number_of_databases < 3:
            raise ValueError("Number of databases cannot be less than 3!")
        self._number_of_databases = number_of_databases
        self._number_of_chunks = self._number_of_databases - 1

    def split(self):
        input_len = len(self._input_string)
        input_enc = self._input_string.encode()
        input_crc = hex(zlib.crc32(input_enc) & 0xffffffff)
        # print("INPUT[length:{0}][CRC:{1}]: '{2}'".format(input_len, input_crc, self._input_string))

        input_b64 = b64encode(input_enc)
        input_b64_crc = hex(zlib.crc32(input_b64) & 0xffffffff)
        input_b64_str = input_b64.decode()
        input_b64_str_len = len(input_b64)
        # print("BASE64[length:{0}][CRC:{1}]: '{2}'".format(input_b64_str_len, input_b64_crc, input_b64_str))

        # @todo: This is not testable this way - needs better separation
        output_object = {
            "input_length":         input_len,
            "input_crc":            input_crc,
            "input_b64_str":        input_b64_str,
            "input_b64_str_len":    input_b64_str_len,
            "input_b64_crc":        input_b64_crc,
        }

        output_json = json.dumps(output_object)
        # print("OUTPUT JSON: {0}".format(output_json))
        output_json_b64_str = b64encode(output_json.encode()).decode()
        output_json_b64_str_len = len(output_json_b64_str)

        if output_json_b64_str_len % 2 != 0:
            raise ValueError("BASE64 string length error! Odd length.")

        self._chunk_length = int(ceil(output_json_b64_str_len / self._number_of_chunks))
        # print("CHUNK LENGTH: {0}".format(self._chunk_length))
        self._chunks = textwrap.wrap(output_json_b64_str, self._chunk_length)

        if len(self._chunks) != self._number_of_chunks:
            raise ValueError("Not enough chunks!")

        self._pad_chunks()

    def create_parity(self):
        parity_bytes = bytearray()
        for li in range(self._chunk_length):
            # print("-" * 30)
            parity_byte = 0
            for ci in range(self._number_of_chunks):
                chunk_char = self._chunks[ci][li]
                chunk_byte = ord(chunk_char)
                # print("Chunk_{0}_char_{1}: {2}({3})".format(ci, li, chunk_char, chunk_byte))
                parity_byte ^= chunk_byte

            parity_bytes.append(parity_byte)
            # print("Parity_byte_{0}: {1}".format(li, hex(parity_byte)))

        # print("Parity_bytes: {0}".format(parity_bytes))
        parity_chunk = b64encode(parity_bytes).decode()
        # print("Parity_chunk: {0}".format(parity_chunk))
        self._chunks.append(parity_chunk)

    def get_chunks(self):
        return self._chunks

    # def dump_chunks(self):
    #     i = 1
    #     for chunk in self._chunks:
    #         print("CHUNK({0})[length:{1}]: '{2}'".format(i, len(chunk), chunk))
    #         i = i + 1

    def _pad_chunks(self):
        for index, chunk in enumerate(self._chunks):
            self._chunks[index] = chunk + '|' * (self._chunk_length - len(chunk))
