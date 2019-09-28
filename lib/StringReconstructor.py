import binascii
import json
import zlib
from base64 import b64decode
from itertools import permutations, islice, count


class StringReconstructor:
    _chunks = None
    _reconstructed_chunk = None
    _parity_bytes = None
    _original_input = None

    def __init__(self, chunks):
        if len(chunks) < 2:
            raise ValueError("Number of chunks must be at least 2!")
        if len(chunks) > 6:
            raise ValueError("Number of chunks can be maximum 6!")

        self._chunks = chunks
        self._check_chunks()

    def get_original_input(self):
        return self._original_input

    def reconstruct(self):
        self._reconstruct_missing_chunk()
        try:
            self._reconstruct_original_input()
        except ValueError:
            raise ValueError("Reconstruction failed.")

    def _reconstruct_original_input(self):
        chunks = self._chunks

        if self._reconstructed_chunk is not None:
            chunks.append(self._reconstructed_chunk)

        number_of_chunks = len(self._chunks)
        # print("Reconstructing from chunks[length: {1}]: {0}".format(chunks, number_of_chunks))

        '''
            The correct order of the chunks is unknown so we need to test them all
            1) we create a list of chunk numbers: order_array
            2) we create a list of all possible combination of orders: order_combinations
            3) we combine the chunks trying each order combination and see if we get a correct answer
        '''
        order_array = []
        for i in islice(count(), number_of_chunks):
            order_array.append(i)

        order_combinations = list(permutations(order_array, len(order_array)))
        # print("Combinations: {0}".format(order_combinations))

        payload_object = None
        for order_array in order_combinations:
            # print("Order: {0}".format(order_array))
            encoded_string = ""
            for current_index in order_array:
                current_chunk = self._chunks[current_index]
                encoded_string += current_chunk

            encoded_string = encoded_string.strip("|")
            # print("Encoded string[{0}]: '{1}'".format(order_array, encoded_string))

            try:
                payload_object = self._get_valid_json(encoded_string)
                self._original_input = self._get_original_input(payload_object)
                break
            except ValueError:
                payload_object = None
                pass

        if payload_object is None:
            raise ValueError("Unable to reconstruct original payload!")

    # noinspection PyMethodMayBeStatic
    def _get_original_input(self, payload_object):
        must_have_keys = ['input_length', 'input_crc', 'input_b64_str', 'input_b64_str_len', 'input_b64_crc']
        keys = list(payload_object.keys())
        has_all_keys = all(elem in keys for elem in must_have_keys)
        if not has_all_keys:
            raise ValueError("Missing keys in payload!")

        if len(payload_object["input_b64_str"]) != payload_object["input_b64_str_len"]:
            raise ValueError("Wrong B64 input length")

        input_b64 = payload_object["input_b64_str"].encode()

        if hex(zlib.crc32(input_b64) & 0xffffffff) != payload_object["input_b64_crc"]:
            raise ValueError("Wrong B64 CRC value")

        input_enc = b64decode(payload_object["input_b64_str"])
        input_string = input_enc.decode()

        if len(input_string) != payload_object["input_length"]:
            raise ValueError("Wrong input length")

        if hex(zlib.crc32(input_string.encode()) & 0xffffffff) != payload_object["input_crc"]:
            raise ValueError("Wrong input CRC value")

        return input_string

    # noinspection PyMethodMayBeStatic
    def _get_valid_json(self, b64_encoded_string):
        try:
            json_string = b64decode(b64_encoded_string)
        except binascii.Error:
            raise ValueError("Unable to b64 decode!")

        try:
            json_object = json.loads(json_string)
        except ValueError:
            raise ValueError("Invalid Json!")
        else:
            return json_object

    def _reconstruct_missing_chunk(self):
        if self._parity_bytes is not None:
            missing_chunk = ""
            number_of_chunks = len(self._chunks)
            chunk_length = len(self._chunks[0])
            missing_chunk_total = 0
            for li in range(chunk_length):
                # print("-" * 30)
                missing_byte = self._parity_bytes[li]
                for ci in range(number_of_chunks):
                    chunk_char = self._chunks[ci][li]
                    chunk_byte = ord(chunk_char)
                    # print("Chunk_{0}_char_{1}: {2}({3})".format(ci, li, chunk_char, chunk_byte))
                    missing_byte ^= chunk_byte

                missing_chunk_total += missing_byte
                missing_char = chr(missing_byte)
                missing_chunk += missing_char
                # print("Missing_byte_{0}: {1}: {2}".format(li, hex(missing_byte), missing_char))

            if missing_chunk_total != 0:
                self._reconstructed_chunk = missing_chunk
                # print("Missing chunk: '{0}'".format(self._reconstructed_chunk))

    def _check_chunks(self):
        # print("Available chunks: '{0}'".format(self._chunks))

        self._extract_parity_chunk()
        # print("Parity Bytes[length:{1}]: {0}".format(self._parity_bytes, len(self._parity_bytes)))
        # print("Available chunks: '{0}'".format(self._chunks))

    def _extract_parity_chunk(self):
        max_chunk_length = self._get_max_chunk_length()
        min_chunk_length = self._get_min_chunk_length(max_chunk_length)
        # print("Chunk lengths: Min:{0} Max:{1}".format(min_chunk_length, max_chunk_length))

        number_of_chunks = len(self._chunks)
        min_length_chunks = 0
        max_length_chunks = 0
        for chunk in self._chunks:
            chunk_length = len(chunk)
            if chunk_length == min_chunk_length:
                min_length_chunks += 1
            elif chunk_length == max_chunk_length:
                max_length_chunks += 1

        if min_length_chunks + max_length_chunks != number_of_chunks:
            raise ValueError("Inconsistent chunk lengths! Only two sizes are allowed.")

        if min_length_chunks != max_length_chunks and max_length_chunks > 1:
            raise ValueError("Inconsistent chunk lengths! Only one parity chunk is allowed.")

        # print("Min length chunks:{0} Max length chunks:{1}".format(min_length_chunks, max_length_chunks))
        if min_length_chunks != number_of_chunks:
            # print("Got available chunks with parity!")
            parity_chunk_index = None
            for index, chunk in enumerate(self._chunks):
                if len(chunk) == max_chunk_length:
                    parity_chunk_index = index

            parity_string = self._chunks[parity_chunk_index]
            del self._chunks[parity_chunk_index]

            # Parity string is b64encoded
            try:
                self._parity_bytes = bytearray(b64decode(parity_string))
            except binascii.Error:
                pass

    def _get_min_chunk_length(self, min_length):
        for chunk in self._chunks:
            chunk_length = len(chunk)
            if chunk_length < min_length:
                min_length = chunk_length
        return min_length

    def _get_max_chunk_length(self):
        max_length = 0
        for chunk in self._chunks:
            chunk_length = len(chunk)
            if chunk_length > max_length:
                max_length = chunk_length
        return max_length
