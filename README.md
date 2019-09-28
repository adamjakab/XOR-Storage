XOR Storage
===========

A proof of concept to show how to achieve a redundancy capable split storage for future cloud use inspired by RAID5 
used on storage arrays. 

The data is first base64 encoded and then split into n equal parts, called chunks. 
Each byte of each chunk is then XOR-ed with the same position byte in the other chunk, hence creating a parity
chunk. The n+1 chunks are stored.

When fetching the chunks the reverse of the operations is executed and the original data is recovered.

However, if you remove one of the storage chunks, data can still be recovered.
Enjoy!  

USAGE
-------
You can store your important data in 5 datastores like this:

`> python3 ./xorstorage.py store "My important data." 5`

If you need it back just ask for it:

`> python3 ./xorstorage.py fetch`

TESTING
-------
`> python3 ./test.py`

