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

# input_string = "Adam was here but now he has left the building. " * 2
# input_string = "ADAM"
# input_string = random_string(generated_input_length)
input_string = "My name is Adam!" * 3

# Splitter
print("-" * 64)
splitter = StringSplitter(input_string, number_of_databases)
splitter.split()
# splitter.dump_chunks()
splitter.create_party()
splitter.dump_chunks()
chunks = splitter.get_chunks()

# Reconstructor - TEST 1
print("-" * 64)
chunk_index = 0
print("Testing with missing chunk[{0}]: '{1}'".format(chunk_index, chunks[chunk_index]))
del chunks[chunk_index]
reconstructor = StringReconstructor(chunks)
reconstructor.reconstruct()




'''
s1 = "a"
s2 = "x"
s3 = "d"

o1 = ord(s1)
o2 = ord(s2)
o3 = ord(s3)
op = 0 ^ o1 ^ o2 ^ o3

print(o1)
print(o2)
print(o3)
print("Parity", op)

m1 = o2 ^ o3 ^ op
print("M1", m1)

m2 = o1 ^ o3 ^ op
print("M2", m2)

m3 = o1 ^ o2 ^ op
print("M2", m3)
'''






