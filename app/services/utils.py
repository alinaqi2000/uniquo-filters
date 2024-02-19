import os
import sqlite3
from Crypto.PublicKey import RSA
import subprocess

# Defining paths and keys
path = os.path.abspath(os.getcwd())
DB_PATH = f"{path}/db/bad_words.db"
BAD_WORDS_DIR = f"{path}/filters/bad_words"
PUBLIC_ENCRYPTION_KEY = "uniquo_public.pem"
PRIVATE_ENCRYPTION_KEY = "uniquo_private.pem"


def get_db_connection():  # Function to establish database connection
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def generate_public_key():  # Function to generate public key
    """Generates a public encryption key if not found."""
    try:
        file = open(key_path(PUBLIC_ENCRYPTION_KEY), 'r')
    except FileNotFoundError:
        subprocess.run(
            f"openssl genpkey -algorithm RSA -out {key_path(PRIVATE_ENCRYPTION_KEY)} -pkeyopt rsa_keygen_bits:2048", shell=True)
        subprocess.run(
            f"openssl rsa -pubout -in {key_path(PRIVATE_ENCRYPTION_KEY)} -out {key_path(PUBLIC_ENCRYPTION_KEY)}", shell=True)
    finally:
        return key_path(PUBLIC_ENCRYPTION_KEY)


def key_path(filename):  # Function to generate key path
    """Returns the full path of the key file."""
    return f"{path}/keys/{filename}"


def read_key(filename):  # Function to read encryption key
    """Reads the encryption key from a file."""
    try:
        key = ""
        with open(f"{path}/keys/{filename}.pem", 'r') as file:
            key = RSA.import_key(file.read())
        return key
    except FileNotFoundError:
        print("File not found:", filename)
        return set()


def read_bad_words():  # Function to read bad words data
    """Reads bad words data from files."""
    try:
        data = {}
        languages = {}

        with open(f"{BAD_WORDS_DIR}/languages.txt", 'r') as file:
            lines = file.readlines()
            for line in lines:
                langs = line.split('->')
                languages[langs[0]] = langs[1]

        for filename in os.listdir(BAD_WORDS_DIR):
            if filename != "languages.txt":
                bad_words = set()
                language_code = filename.split('.')[0]
                with open(f"{BAD_WORDS_DIR}/{filename}", 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        words = [word.strip() for word in line.split(',')]
                        bad_words = bad_words.union(words)
                data[language_code] = bad_words

        return languages, data
    except FileNotFoundError:
        print("File not found:", filename)
        return set()
