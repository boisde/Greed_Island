import gnupg
import os.path
import shutil

class GpgEncrypt:
    def __init__(self):
        gnupg_path = os.path.dirname(os.path.abspath(__file__))+'/.gnupg'
        # clean up keys if exist
        if os.path.exists(gnupg_path):
            print 'exist'
            shutil.rmtree(gnupg_path)
        else:
            print 'not exist'
        self.exported_key_file = gnupg_path+'/exported_key.private'
        self.gnupg_path = gnupg_path[:-7]
        gpg = gnupg.GPG(gnupghome=gnupg_path)
        gpg.encoding = 'utf-8'
        key = gpg.gen_key(gpg.gen_key_input(key_type="RSA", key_length=1024))
        self.gpg = gpg
        self.fp = key.fingerprint
        ascii_armored_private_keys=gpg.export_keys(self.fp, True)
        with open(self.exported_key_file, 'w') as the_key:
            the_key.write(ascii_armored_private_keys)
        print 'Export pk:[%s]' % self.exported_key_file

    def do_encrypt(self, file_path):
        self.encoded_file = file_path+'.encoded'
        savefile = file_path+'.decoded'
        #encryption
        with open(file_path, 'rb') as content_file:
            data = content_file.read()
            encrypted_ascii_data = str(self.gpg.encrypt(data, self.fp, output=self.encoded_file))
            print 'encrypted_data=[%s]' % self.encoded_file
            #decryption
            self.gpg.decrypt(encrypted_ascii_data, output=savefile)
            print 'decrypted_data=[%s]'% savefile
    
    def delete_key(self):
        #delete key
        print str(self.gpg.delete_keys(self.fp, True))
        print str(self.gpg.delete_keys(self.fp))




#    data = raw_input("Enter full path of file to encrypt:")
#    rkeys = raw_input("Enter key IDs seperated by spaces:")
#    savefile = data+".asc"
#    afile = open(data, "rb")
#    encrypted_ascii_data = gpg.encrypt_file(afile, rkeys.split(), always_trust=True, output=savefile)
#    afile.close()


if __name__ == '__main__':
    encryptor=GpgEncrypt()
    encryptor.do_encrypt('/home/alice/Music/kite.mp3')
    encryptor.delete_key()
