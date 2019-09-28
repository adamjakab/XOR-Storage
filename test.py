import string
import random
from itertools import islice, count

from lib.StringSplitter import StringSplitter
from lib.StringReconstructor import StringReconstructor


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.digits + string.ascii_letters + string.punctuation
    return ''.join(random.choice(letters) for i in range(string_length))


# Variables
generated_input_length = 128
number_of_databases = 3

input_string = "ADAM WAS HERE!" * 3
# input_string = "ADAM"
# input_string = random_string(generated_input_length)
# input_string = "My name is Adam!" * 3

# Splitter
print("-" * 64)
print("Original input: '{0}'".format(input_string))
splitter = StringSplitter(input_string, number_of_databases)
splitter.split()
splitter.create_parity()
splitter.dump_chunks()
chunks = splitter.get_chunks()


# Reconstructor - TESTS
print("\n" + "*" * 64)
print("RUNNING TESTS")
print("*" * 64)

# This array will tell which chunk to remove during testing (None means no chunks are removed)
index_array = [None]
for i in islice(count(), number_of_databases):
    index_array.append(i)

for chunk_index in index_array:
    print("-" * 64)
    print("TESTING WITH MISSING CHUNK: {}".format(chunk_index))
    test_chunks = chunks.copy()
    if chunk_index is not None:
        del test_chunks[chunk_index]
    reconstructor = StringReconstructor(test_chunks)
    reconstructor.reconstruct()
    reconstructed_input = reconstructor.get_original_input()
    if input_string != reconstructed_input:
        raise ValueError("Reconstructed input does not match original input")
    else:
        print("Got matching reconstructed input: '{0}'".format(reconstructed_input))
