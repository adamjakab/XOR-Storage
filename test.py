import string
import random
from lib.StringSplitter import StringSplitter
from lib.StringReconstructor import StringReconstructor


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.digits + string.ascii_letters + string.punctuation
    return ''.join(random.choice(letters) for i in range(string_length))


# Variables
generated_input_length = 128
number_of_databases = 4

input_string = "ADAM WAS HERE!"
# input_string = "ADAM"
# input_string = random_string(generated_input_length)
# input_string = "My name is Adam!" * 3

# Splitter
print("-" * 64)
splitter = StringSplitter(input_string, number_of_databases)
splitter.split()
splitter.create_parity()
splitter.dump_chunks()
chunks = splitter.get_chunks()

# Reconstructor - TEST 1
print("-" * 64)
chunk_index = 0
print("Testing with missing chunk[{0}]: '{1}'".format(chunk_index, chunks[chunk_index]))
del chunks[chunk_index]
reconstructor = StringReconstructor(chunks)
reconstructor.reconstruct()





