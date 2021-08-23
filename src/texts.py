import os

def get_text(path='./data/full_contract_txt/', n=0):
# read the first contract in the folder to a variable
    filenm = os.listdir(path)[n]
    full_path = path + filenm
    f = open(full_path, 'r')
    return f.read()

if __name__ == '__main__':
    print(get_text())