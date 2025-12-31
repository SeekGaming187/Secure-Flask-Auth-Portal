from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import os

class Server:
    def __init__(self):
        """
        Initializes the Server class.

        This constructor sets up the initial state of the Server instance, including loading RSA keys,
        setting the database path, and initializing various attributes.

        Attributes:
            database_path (str): The path to the database file.
            public_key (RSA.RsaKey): The RSA public key for encryption.
            private_key (RSA.RsaKey): The RSA private key for decryption.
            index (int): A counter used for OTP validation.
            register_otp (str): The initial OTP value used during registration.
            otp_mod (int): The modulus value used for OTP generation and validation.
        """
        self.database_path = "database.txt"
        self.public_key = RSA.import_key(open("public.pem").read())
        self.private_key = RSA.import_key(open("private.pem").read())
        self.index = 0
        self.register_otp = "000000"
        self.otp_mod = 99  # You can change this value if needed. Default is 100-1  99.

    def encrypt_line(self, line):
        """
        Encrypts a line of text using the RSA public key.

        Args:
            line (str): The line of text to be encrypted.

        Returns:
            bytes: The encrypted line of text in bytes.
        """

        cipher_rsa = PKCS1_OAEP.new(self.public_key)
        return cipher_rsa.encrypt(bytes(line, 'utf-8'))

    def decrypt_line(self, encrypted_line):
        """
        Decrypts an encrypted line of text using the RSA private key.

        Args:
            encrypted_line (bytes): The encrypted line of text in bytes.

        Returns:
            str: The decrypted line of text as a string.
        """
        cipher_rsa = PKCS1_OAEP.new(self.private_key)
        return cipher_rsa.decrypt(encrypted_line).decode()

    def load_database(self):
        """
        Loads the database from the file, decrypting each line.

        This method reads the encrypted database file, decrypts each line, and returns the data as a list of lists.

        Returns:
            list: A list of lists, where each inner list represents a database entry.
        """
        if os.path.exists(self.database_path):
            decrypted_lines = []
            with open(self.database_path, "rb") as file:
                while True:
                    line_size = file.read(4)
                    if not line_size:
                        break
                    line_size = int.from_bytes(line_size, "big")
                    encrypted_line = file.read(line_size)
                    decrypted_line = self.decrypt_line(encrypted_line)
                    decrypted_lines.append(decrypted_line)
            return [line.split(";") for line in decrypted_lines]
        return []

    def save_database(self, database):
        """
        Saves the database to the file, encrypting each line.

        This method writes the database to the file, encrypting each line and storing the size of each encrypted line.

        Args:
            database (list): A list of lists, where each inner list represents a database entry.
        """

        with open(self.database_path, "wb") as file:
            for line in database:
                data = ";".join(line)
                encrypted_line = self.encrypt_line(data)
                file.write(len(encrypted_line).to_bytes(4, "big"))
                file.write(encrypted_line)

    def register_user(self, username, hashed_password, otp_token):

        """
        Registers a new user with the given username, hashed password, and OTP token.

        This method checks if the username already exists in the database. If it does, registration fails.
        If the username is unique, it adds the new user to the database and saves the updated database.

        Args:
            username (str): The username of the new user.
            hashed_password (str): The hashed password of the new user.
            otp_token (str): The initial OTP token for the new user.

        Returns:
            bool: True if the registration is successful, False if the username already exists.
        """

        try:
            database = self.load_database()
            for entry in database:
                if entry[0] == username:
                    return False
            database.append([username, hashed_password, otp_token, '0'])
            self.register_otp = otp_token
            self.save_database(database)
            return True
        except Exception as e:
            raise(e)

    def verify_login(self, username, hashed_password):
        """
        Verifies the login credentials of a user.

        This method checks if the provided username and hashed password match any entry in the database.

        Args:
            username (str): The username to verify.
            hashed_password (str): The hashed password to verify.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        database = self.load_database()
        for entry in database:
            if entry[0] == username and entry[1] == hashed_password:
                return True
        return False

    def validate_otp(self, username, client_otp):
        """
        Validates the OTP (One-Time Password) for a user.

        This method checks if the provided OTP matches the expected OTP for the user.
        If the OTP is valid, it updates the OTP counter and the stored OTP for the user.

        Args:
            username (str): The username to validate the OTP for.
            client_otp (str): The OTP provided by the client.

        Returns:
            bool: True if the OTP is valid, False otherwise.
        """
        database = self.load_database()
        for entry in database:
            if entry[0] == username:
                counter = int(entry[3])

                if(self.index % self.otp_mod == 0):
                    self.index = 0
                    entry[2] = self.register_otp


                hashed_client_otp = self.hash_one_time_otp(client_otp)
                if entry[2] == hashed_client_otp:
                    entry[3] = str(counter + 1)
                    entry[2] = client_otp
                    self.index = self.index + 1
                    self.save_database(database)
                    return True
        return False


    def hash_one_time_otp(self ,client_otp):
        """
        Hashes a single OTP value using SHA256.
        """
        hash_obj = SHA256.new(bytes.fromhex(client_otp))
        return hash_obj.digest().hex()