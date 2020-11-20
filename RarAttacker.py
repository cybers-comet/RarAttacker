from unrar import rarfile
import optparse
import sys
import threading
from threading import Thread
import os
import time
from colorama import Fore, Back, Style

# the flag of the end of the program
status = 0

# lock the screen's output
screenLock = threading.Semaphore(1)


def interface():
    os.system("CLS")
    print("""
      _____                  _   _             _             
      |  __ \            /\  | | | |           | |            
      | |__) |__ _ _ __ /  \ | |_| |_ __ _  ___| | _____ _ __ 
      |  _  // _` | '__/ /\ \| __| __/ _` |/ __| |/ / _ \ '__|
      | | \ \ (_| | | / ____ \ |_| || (_| | (__|   <  __/ |   
      |_|  \_\__,_|_|/_/    \_\__|\__\__,_|\___|_|\_\___|_|                                                          
                                                         
    """)
    print(Back.BLUE + "Author   : Cyberscomet" + Style.RESET_ALL)
    print(Back.BLUE + "Time   : 2020-11-20" + Style.RESET_ALL)
    print(Back.BLUE + "github   : https://github.com/cybers-comet" + Style.RESET_ALL)


# extract the password
def extractFile(rFile, password):
    global status
    try:
        screenLock.acquire()
        rFile.extractall(pwd=password)
        status = 1
        print(Back.GREEN + '-----------------------------------')
        print(Back.GREEN + '[+] [' + str(time.asctime()) + '] Found password: ' + str(password) + '          ')
        print(Back.GREEN + '-----------------------------------')
        print(Style.RESET_ALL)
        screenLock.release()
    except:
        print(Back.RED + '[+] [' + str(time.asctime()) + '] Error password:' + str(password)+Style.RESET_ALL)
        screenLock.release()


# include the rarfile and dictionary file
def main():
    parser = optparse.OptionParser('usage%prog ' + '-f <rarfile> -d <dictionary>')
    parser.add_option('-f', dest='rname', type='string', help='specify rar file')
    parser.add_option('-d', dest='dname', type='string', help='specify dictionary file')
    (options, args) = parser.parse_args()
    if (options.rname == None) or (options.dname == None):
        print(parser.usage)
        exit(0)
    else:
        interface()
        rname = options.rname
        dname = options.dname
    rFile = rarfile.RarFile(rname, mode='r')
    pwdFile = open(dname, 'r')
    print(Back.BLUE + 'Loading dictionary file,Please wait...' + Style.RESET_ALL)
    try:
        text_lines = pwdFile.readlines()
        for line in text_lines:
            password = line.strip('\n')
            t = Thread(target=extractFile, args=(rFile, password))
            # t.setDaemon(True)
            t.start()
            t.join()
            if status == 1:
                sys.exit(0)
    except Exception:
        print('[!] Error:' + str(Exception))
        print('RarAttacker didn\'t find the password,Please try another dictionary again!  ')
    finally:
        pwdFile.close()


if __name__ == '__main__':
    main()
