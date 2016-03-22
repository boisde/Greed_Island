import gnupg
import os.path


class GpgEncrypt:
    def __init__(self):
        self.encrypted_file = ''
        self.try_decoded_file = ''
        self.exported_private_key_file = os.path.dirname(os.path.abspath(__file__)) + '/exported_key.private'
        self.exported_public_key_file = os.path.dirname(os.path.abspath(__file__)) + '/exported_key.public'
        gnupg_path = os.path.dirname(os.path.abspath(__file__)) + '/.gnupg'
        self.gpg = gnupg.GPG(gnupghome=gnupg_path)
        self.gpg.encoding = 'utf-8'
        # import public key if exist
        if os.path.exists(self.exported_public_key_file):
            print 'exist'
            with open(self.exported_public_key_file, 'rb') as key_file:
                key_data = key_file.read()
                import_result = self.gpg.import_keys(key_data)
                self.fp = import_result.fingerprints
                print('Imported public key fingerprint:[%s]' % self.fp)
        # run at the first time, generate and export key pair
        else:
            print 'the first time'
            key = self.gpg.gen_key(self.gpg.gen_key_input(key_type="RSA", key_length=1024))
            self.fp = key.fingerprint
            ascii_armored_public_keys = self.gpg.export_keys(self.fp)
            ascii_armored_private_keys = self.gpg.export_keys(self.fp, True)
            with open(self.exported_public_key_file, 'w') as the_public_key:
                the_public_key.write(ascii_armored_public_keys)
            print('Exported public key:[%s]' % self.exported_public_key_file)
            with open(self.exported_private_key_file, 'w') as the_key:
                the_key.write(ascii_armored_private_keys)
            print('Exported private key:[%s]' % self.exported_private_key_file)

    # store both encrypted and locally decrypted file
    def do_encrypt(self, file_path):
        self.encrypted_file = file_path + '.encoded'
        self.try_decoded_file = file_path + '.decoded'
        # encryption
        with open(file_path, 'rb') as content_file:
            data = content_file.read()
            encrypted_ascii_data = str(self.gpg.encrypt(data, self.fp, output=self.encrypted_file))
            print('Encrypted_data=[%s]' % self.encrypted_file)
            # decryption
            self.gpg.decrypt(encrypted_ascii_data, output=self.try_decoded_file)
            print('Decrypted_data=[%s]' % self.try_decoded_file)
            return self.encrypted_file

    def delete_key(self):
        print('Delete GPG private key:[%s]' % str(self.gpg.delete_keys(self.fp, True)))
        print('Delete GPG public key:[%s]' % str(self.gpg.delete_keys(self.fp)))


# data = raw_input("Enter full path of file to encrypt:")
#    rkeys = raw_input("Enter key IDs seperated by spaces:")
#    savefile = data+".asc"
#    afile = open(data, "rb")
#    encrypted_ascii_data = gpg.encrypt_file(afile, rkeys.split(), always_trust=True, output=savefile)
#    afile.close()


if __name__ == '__main__':
    encryptor = GpgEncrypt()
    encryptor.do_encrypt('/home/alice/Music/kite.mp3')
    encryptor.delete_key()
