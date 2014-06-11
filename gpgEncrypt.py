import gnupg

def test():
    gpg = gnupg.GPG(gnupghome='/home/alice/Developer/Greed_Island/')
    gpg.encoding = 'utf-8'

    input_data = gpg.gen_key_input(key_type="RSA", key_length=1024)
    key = gpg.gen_key(input_data)
    print key


if __name__ == '__main__':
    test()
