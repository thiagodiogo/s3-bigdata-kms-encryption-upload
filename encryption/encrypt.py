import aws_encryption_sdk
import datetime, os, sys

key_id = sys.argv[1]
plaintext_filename = sys.argv[2]
ciphertext_filename = sys.argv[3]

kms_key_provider = aws_encryption_sdk.KMSMasterKeyProvider(key_ids=[
    key_id
])

print("Plain file to be encrypted: %s" % plaintext_filename)
print("Details: %s" % os.stat(plaintext_filename))

start = datetime.datetime.now()
print("Starting at %s" % start)

with open(plaintext_filename, 'rb') as pt_file, open(ciphertext_filename, 'wb') as ct_file:
    with aws_encryption_sdk.stream(
        mode='e',
        source=pt_file,
        key_provider=kms_key_provider
    ) as encryptor:
        for chunk in encryptor:
            ct_file.write(chunk)

print("File encrypted: %s" % ciphertext_filename)
print("Details: %s" % os.stat(ciphertext_filename))

end = datetime.datetime.now()
print("Ending at %s" % end)
print("Total elapsed time: %s" % (end-start))
