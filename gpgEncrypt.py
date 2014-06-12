import gnupg

def test():
    #key generation
    gpg = gnupg.GPG(gnupghome='./.gnupg'#, verbose=Truei
            )
    gpg.encoding = 'utf-8'
    key = gpg.gen_key(gpg.gen_key_input())
    fp = key.fingerprint
    print 'key=[%s], fingerprint=[%s]'% (key, fp)
    gpg.list_keys(True)

#    data = raw_input("Enter full path of file to encrypt:")
#    rkeys = raw_input("Enter key IDs seperated by spaces:")
#    savefile = data+".asc"
#    afile = open(data, "rb")
#    encrypted_ascii_data = gpg.encrypt_file(afile, rkeys.split(), always_trust=True, output=savefile)
#    afile.close()
#    input_data = gpg.gen_key_input(key_type="RSA", key_length=1024)
#    key = gpg.gen_key(input_data)

    #encryption
    with open('./README.md', 'rb') as content_file:
        data = content_file.read()
        print 'raw=[%s]'%data
        encrypted_ascii_data = gpg.encrypt(str(data),fp)
        print 'encrypted=[%s]'%encrypted_ascii_data
        #decryption
        decrypted_data = gpg.decrypt(str(encrypted_ascii_data))
        print 'decrypted_data=[%s]'%decrypted_data

    #delete key
    print str(gpg.delete_keys(fp, True))
    print str(gpg.delete_keys(fp))

if __name__ == '__main__':
    test()
