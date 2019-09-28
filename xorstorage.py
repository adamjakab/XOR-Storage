import argparse
import os

from lib.StringReconstructor import StringReconstructor
from lib.StringSplitter import StringSplitter

storage_folder = "./storage"

# Add command line arguments and run
parser = argparse.ArgumentParser(description='XOR Storage')
# parser.add_argument('--store', action='store_true', default=False, help='Store your data')
parser.add_argument('action', choices=['store', 'fetch'], type=str, help='Your action: store or fetch')
parser.add_argument('data', metavar='DATA', nargs='?', type=str, help='The data to store')
parser.add_argument('num_db', metavar='NUM_DB', default=3, nargs='?', type=int, choices=range(3, 7), help='Number of databases(3-6)')
args = parser.parse_args()


def store_data():
    input_string = args.data
    number_of_databases = args.num_db
    # print("STORING[db:{0}] YOUR DATA: '{1}'".format(number_of_databases, input_string))

    # Split data
    splitter = StringSplitter(input_string, number_of_databases)
    splitter.split()
    splitter.create_parity()
    chunks = splitter.get_chunks()

    # Make storage directory
    if not os.path.exists(storage_folder):
        os.makedirs(storage_folder)

    # Clean up storage directory
    for the_file in os.listdir(storage_folder):
        file_path = os.path.join(storage_folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    # Store chunks
    for i, chunk in enumerate(chunks, start=1):
        file_path = os.path.join(storage_folder, "db_{0}.txt".format(i))
        with open(file_path, "w") as db_file:
            db_file.write(chunk)

    print("Data is stored in {0} files under the '{1}' folder.".format(number_of_databases, storage_folder))


def fetch_data():
    chunks = []

    # Fetch content of storage files
    for the_file in os.listdir(storage_folder):
        file_path = os.path.join(storage_folder, the_file)
        with open(file_path, "r") as db_file:
            chunks.append(db_file.read())

    reconstructor = StringReconstructor(chunks)
    try:
        reconstructor.reconstruct()
    except ValueError as e:
        print("Error: {0}".format(e))
        print("Not enough information to reconstruct your data.")
    else:
        reconstructed_input = reconstructor.get_original_input()
        print("Stored data was: '{0}'".format(reconstructed_input))


if __name__ == '__main__':
    if args.action == "store":
        store_data()
    elif args.action == "fetch":
        fetch_data()
    else:
        parser.print_help()
