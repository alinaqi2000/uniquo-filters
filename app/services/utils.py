import os
import sqlite3
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import subprocess

path = os.path.abspath(os.getcwd())
DB_PATH = f"{path}/db/bad_words.db"
PUBLIC_ENCRYPTION_KEY = "uniquo_public.pem"
PRIVATE_ENCRYPTION_KEY = "uniquo_private.pem"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def generate_public_key():
    try:
        file = open(key_path(PUBLIC_ENCRYPTION_KEY), 'r')

    except FileNotFoundError:
        subprocess.run(
            f"openssl genpkey -algorithm RSA -out {key_path(PRIVATE_ENCRYPTION_KEY)} -pkeyopt rsa_keygen_bits:2048", shell=True)
        subprocess.run(
            f"openssl rsa -pubout -in {key_path(PRIVATE_ENCRYPTION_KEY)} -out {key_path(PUBLIC_ENCRYPTION_KEY)}", shell=True)

    finally:
        return key_path(PUBLIC_ENCRYPTION_KEY)


def key_path(filename):
    return f"{path}/keys/{filename}"


def read_key(filename):
    try:
        key = ""
        with open(f"{path}/keys/{filename}.pem", 'r') as file:
            key = RSA.import_key(file.read())
        return key
    except FileNotFoundError:
        print("File not found:", filename)
        return set()


def read_bad_words(filename):
    try:
        bad_words_set = set()
        with open(f"{path}/filters/{filename}", 'r') as file:
            lines = file.readlines()
            for line in lines:
                words = [word.strip() for word in line.split(',')]
                bad_words_set = bad_words_set.union(words)
        return bad_words_set
    except FileNotFoundError:
        print("File not found:", filename)
        return set()
