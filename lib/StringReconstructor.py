from string import *
from base64 import b64encode, b64decode
from itertools import product, permutations, islice, count


class StringReconstructor:
    _chunks = None
    _reconstructed_chunk = None
    _parity_bytes = None
    _original_input = None

    def __init__(self, chunks):
        self._chunks = chunks

    def reconstruct(self):
        self._check_chunks()
        self._reconstruct_missing_chunk()
        self._reconstruct_original_input()

    def _reconstruct_original_input(self):
        chunks = self._chunks
        if self._reconstructed_chunk is not None:
            chunks.append(self._reconstructed_chunk)

        number_of_chunks = len(self._chunks)
        print("All Chunks[length: {1}]: {0}".format(chunks, number_of_chunks))

        # The correct order is unknown so we need to test them all
        order_array = []
        for i in islice(count(), number_of_chunks):
            order_array.append(i)

        order_combinations = permutations(order_array, len(order_array))

        for order_array in list(order_combinations):
            # print("Order: {0}".format(order_array))
            encoded_string = ""
            for current_index in order_array:
                current_chunk = self._chunks[current_index].strip("|")
                encoded_string += current_chunk

            original_string = b64decode(encoded_string)
            print("Encoded string[{0}]: '{1}' => '{2}'".format(order_array, encoded_string, original_string))



    def _reconstruct_missing_chunk(self):
        if self._parity_bytes is not None:
            missing_chunk = ""
            number_of_chunks = len(self._chunks)
            chunk_length = len(self._chunks[0])
            for li in range(chunk_length):
                # print("-" * 30)
                missing_byte = self._parity_bytes[li]
                for ci in range(number_of_chunks):
                    chunk_char = self._chunks[ci][li]
                    chunk_byte = ord(chunk_char)
                    # print("Chunk_{0}_char_{1}: {2}({3})".format(ci, li, chunk_char, chunk_byte))
                    missing_byte ^= chunk_byte

                missing_char = chr(missing_byte)
                missing_chunk += missing_char
                # print("Missing_byte_{0}: {1}: {2}".format(li, hex(missing_byte), missing_char))

            self._reconstructed_chunk = missing_chunk
            print("Missing chunk: {0}".format(self._reconstructed_chunk))

    def _check_chunks(self):
        print("Available chunks: '{0}'".format(self._chunks))

        self._extract_parity_chunk()
        print("Parity Bytes[length:{1}]: {0}".format(self._parity_bytes, len(self._parity_bytes)))
        print("Available chunks: '{0}'".format(self._chunks))

    def _extract_parity_chunk(self):
        max_chunk_length = self._get_max_chunk_length()
        min_chunk_length = self._get_min_chunk_length(max_chunk_length)
        print("Chunk lengths: Min:{0} Max:{1}".format(min_chunk_length, max_chunk_length))

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
            raise ValueError("Inconsistent chunk lengths!")

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
            self._parity_bytes = bytearray(b64decode(parity_string))

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
