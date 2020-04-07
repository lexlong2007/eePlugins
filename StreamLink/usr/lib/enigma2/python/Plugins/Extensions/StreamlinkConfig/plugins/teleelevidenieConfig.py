import sys

if __name__ == '__main__' and len(sys.argv) >=5:
    username = sys.argv[1]
    password = sys.argv[2]
    filename = sys.argv[3]
    streamlinkURL = 'http%3a//127.0.0.1%3a%s/' % sys.argv[4]
