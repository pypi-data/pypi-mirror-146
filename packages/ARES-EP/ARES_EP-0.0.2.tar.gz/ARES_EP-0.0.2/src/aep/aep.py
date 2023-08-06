#!/usr/bin/env python

from pydoc import plain
import sys
import math
from os.path import exists

testKey = "PeSgVkYp3s6v9y$B&E)H@McQfTjWmZq4t7w!z%C*F-JaNdRgUkXp2r5u8x/A?D(G+KbPeShVmYq3t6v9y$B&E)H@McQfTjWnZr4u7x!z%C*F-JaNdRgUkXp2s5v8y/B?D(G+KbPeShVmYq3t6w9z$C&F)H@McQfTjWnZr4u7x!A%D*G-KaNdRgUkXp2s5v8y/B?E(H+MbQeThVmYq3t6w9z$C&F)J@NcRfUjXnZr4u7x!A%D*G-KaPdSgVkYp3s5v8y/B?E(H+MbQeThWmZq4t7w9z$C&F)J@NcRfUjXn2r5u8x/A%D*G-KaPdSgVkYp3s6v9y$B&E(H+MbQeThWmZq4t7w!z%C*F-J@NcRfUjXn2r5u8x/A?D(G+KbPdSgVkYp3s6v9y$B&E)H@McQfThWmZq4t7!z%C*F-JaNdRgUkXn2r5u8x/A?D(G+KbPeShVmYq3s6v9y$B&E)H@McQfTjWnZr4u7w!z%C*F-JaNdRgUkXp2s5v8y/A?D(G+Kb"

def encrypt(message, key):
    # Layer 1: Exponential Encoding
    messageArray = []
    for i in message:
        messageArray.append(i)

    keyArray = []
    for i in key:
        keyArray.append(i)

    encryptedPreBinary = []
    for i in range(len(message)):
        encryptedPreBinary.append(math.floor(math.exp(ord(messageArray[i]))))

    keyEncrypted = []
    for i in range(len(keyArray)):
        keyEncrypted.append(ord(keyArray[i]))

    # Layer 2: XOR Encryption

    binaryKey = ""
    for i in range(len(keyEncrypted)):
        binaryKey += f'{keyEncrypted[i]:08b}'

    binaryMessage = ""
    for i in range(len(encryptedPreBinary)):
        binaryMessage += f'{encryptedPreBinary[i]:0190b}'

    xor = ""
    for i in range(len(binaryMessage)):
        if binaryMessage[i] == binaryKey[i]:
            xor += "0"
        else:
            xor += "1"
    
    # Layer 3: Random Character Substitution

    # split xor into 8 bit chunks
    xorArray = []
    for i in range(0, len(xor), 8):
        xorArray.append(xor[i:i+8])
    
    # convert each 8 bit chunk to decimal
    xordecimal = []
    for i in range(len(xorArray)):
        # if (int(xorArray[i], 2) >= 100) or (int(xorArray[i], 2) < 20) or (chr(int(xorArray[i], 2)) == '0') or (chr(int(xorArray[i], 2)) == '1'):
        if (chr(int(xorArray[i], 2)) == '0') or (chr(int(xorArray[i], 2)) == '1'):
            xordecimal.append(xorArray[i])
        elif (int(xorArray[i], 2)) < 32 or (int(xorArray[i], 2)) > 126:
            xordecimal.append(xorArray[i])
        else:
            xordecimal.append(chr(int(xorArray[i], 2)))

    # join xordecimal
    xordecimal = "".join(str(x) for x in xordecimal)

    return xordecimal

def decrypt(encrypted, key):

    # Layer 1: Random Character Substitution:

    xorArray = []
    count = 0
    while count < len(encrypted):
        if (encrypted[count] == '1') or (encrypted[count] == '0'):
            xorArray.append(encrypted[count:count+8])
            count += 8
        else:
            xorArray.append(f'{int(ord(encrypted[count:count+1])):08b}')
            count += 1

    rcs = "".join(str(x) for x in xorArray)

    # Layer 2: XOR Decryption

    keyArray = []
    for i in key:
        keyArray.append(i)

    keyEncrypted = []
    for i in range(len(keyArray)):
        keyEncrypted.append(ord(keyArray[i]))

    binaryKey = ""
    for i in range(len(keyEncrypted)):
        binaryKey += f'{keyEncrypted[i]:08b}'
    
    xor = ""
    for i in range(len(rcs)):
        if rcs[i] == binaryKey[i]:
            xor += "0"
        else:
            xor += "1"
    
    xorArray = []
    for i in range(0, len(xor), 190):
        xorArray.append(xor[i:i+190])
    
    xordecimal = []
    for i in range(len(xorArray)):
        xordecimal.append(int(xorArray[i], 2))

    # Layer 3: Exponential Decoding

    xorLog = []
    for i in range(len(xordecimal)):
        xorLog.append(int(math.log(xordecimal[i])))

    xorChar = []
    for i in range(len(xorLog)):
        if xorLog[i] == 31:
            xorChar.append(' ')
        else:
            xorChar.append(chr(xorLog[i]))

    xorChar = "".join(xorChar)
    return xorChar

def generateKeyPair(name, passphrase, testKey):
    while (len(passphrase) < len(name) * 20):
        passphrase += passphrase
    while (len(testKey) < len(passphrase) * 32):
        testKey += testKey
    passphrase2 = keySchedule(passphrase)
    pubKey = encrypt(name, passphrase2)
    privKey = encrypt(passphrase, testKey)
    return pubKey, privKey

def pubKeyEncrypt(plaintext, pubKey):
    return encrypt(plaintext, pubKey)

def privKeyDecrypt(encrypted, privKey, name, testKey):
    passphrase = input("What is your password?")
    while (len(passphrase) < len(name) * 20):
        passphrase += passphrase
    while (len(testKey) < len(passphrase) * 32):
        testKey += testKey
    expectedPrivKey = encrypt(passphrase, testKey)
    if (privKey == expectedPrivKey):
        passphrase2 = keySchedule(passphrase)
        pubKey = encrypt(name, passphrase2)

        return (decrypt(encrypted, pubKey))

def keySchedule(key):
    # convert to binary
    keyBinary = []
    for i in key:
        keyBinary.append(f'{ord(i):08b}')

    subKeys = []
    for i in range(len(keyBinary)):
        if (i == 0):
            currXor = ""
            for j in range(len(keyBinary[i])):
                if keyBinary[i][j] == keyBinary[15][j]:
                    currXor += "0"
                else:
                    currXor += "1"
            subKeys.append(currXor)
        else:
            currXor = ""
            for j in range(len(keyBinary[i])):
                if keyBinary[i][j] == subKeys[i-1][j]:
                    currXor += "0"
                else:
                    currXor += "1"
            subKeys.append(currXor)

    for i in range(len(subKeys)):
        if (i == 0):
            currXor = ""
            for j in range(len(subKeys[i])):
                if subKeys[i][j] == subKeys[15][j]:
                    currXor += "0"
                else:
                    currXor += "1"
            subKeys[i] = currXor
        else:
            currXor = ""
            for j in range(len(subKeys[i])):
                if subKeys[i][j] == subKeys[i-1][j]:
                    currXor += "0"
                else:
                    currXor += "1"
            subKeys[i] = currXor
    
    # join subkeys
    subKeys = "".join(str(x) for x in subKeys)
    return subKeys

if sys.argv[1] == '-gen':
    if (len(sys.argv) == 6):
        keys = generateKeyPair(sys.argv[2], sys.argv[3], testKey)
        if (exists(sys.argv[4])):
            f = open(sys.argv[4], "w")
            f.write(keys[0])
            f.close()
        else:
            f = open(sys.argv[4], "x")
            f.write(keys[0])
            f.close()

        if (exists(sys.argv[5])):
            f = open(sys.argv[5], "w")
            f.write(keys[1])
            f.close()
        else:
            f = open(sys.argv[5], "x")
            f.write(keys[1])
            f.close()
    else:
        print('Too many or too few arguments')
elif(sys.argv[1] == '-pubEnc'):
    if (len(sys.argv) == 5):
        if (exists(sys.argv[2])):
            f = open(sys.argv[2], "r")
            plaintext = f.read()
            f.close()
        else:
            print('Plaintext file does not exist')
            exit()
        
        if (exists(sys.argv[3])):
            f = open(sys.argv[3], "r")
            pubKey = f.read()
            f.close()
        else:
            print('Public key file does not exist')
            exit()

        encrypted = pubKeyEncrypt(plaintext, pubKey)
        if (exists(sys.argv[4])):
            f = open(sys.argv[4], "w")
            f.write(encrypted)
            f.close()
        else:
            f = open(sys.argv[4], "x")
            f.write(encrypted)
            f.close()

    else:
        print('Too many or too few arguments')
elif(sys.argv[1] == '-privDec'):
    if (len(sys.argv) == 6):
        if (exists(sys.argv[2])):
            f = open(sys.argv[2], "r")
            encrypted = f.read()
            f.close()
        else:
            print('Encrypted file does not exist')
            exit()
        
        if (exists(sys.argv[3])):
            f = open(sys.argv[3], "r")
            privKey = f.read()
            f.close()
        else:
            print('Private key file does not exist')
            exit()

        decrypted = privKeyDecrypt(encrypted, privKey, sys.argv[4], testKey)
        if (decrypted == None):
            print('Invalid private key')
        else:
            if (exists(sys.argv[5])):
                f = open(sys.argv[5], "w")
                f.write(decrypted)
                f.close()
            else:
                f = open(sys.argv[5], "x")
                f.write(decrypted)
                f.close()
    else:
        print('Too many or too few arguments')
elif (sys.argv[1] == '-help') or (sys.argv[1] == '-h'):
    print('-gen [name] [passphrase] [save pubKey file path] [save privKey file path]: Generates a public and private key pair')
    print('-pubEnc [plaintext file path] [pubKey file path] [save encrypted file path]: Encrypts a plaintext with a public key')
    print('-privDec [encrypted file path] [privKey file path] [name] [save decrypted file path]: Decrypts an encrypted message with a private key')
    print('-help: Prints this message')
else:
    print('Invalid command')
