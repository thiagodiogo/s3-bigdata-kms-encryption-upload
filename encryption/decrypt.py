import aws_encryption_sdk
import datetime, os, sys

key_id = sys.argv[1]

cipher_filename = sys.argv[2]
decrypted_file = sys.argv[3]

kms_key_provider = aws_encryption_sdk.KMSMasterKeyProvider(key_ids=[
    key_id
])

print("Encrypted file to be decrypted: %s" % cipher_filename)
print("Details: %s" % os.stat(cipher_filename))

start = datetime.datetime.now()
print("Starting at %s" % start)

with open(cipher_filename, 'rb') as ct_file, open(decrypted_file, 'wb') as pt_file:
    with aws_encryption_sdk.stream(
        mode='d',
        source=ct_file,
        key_provider=kms_key_provider
    ) as decryptor:
        for chunk in decryptor:
            pt_file.write(chunk)

print("File decrypted: %s" % decrypted_file)
print("Details: %s" % os.stat(decrypted_file))

end = datetime.datetime.now()
print("Ending at %s" % end)
