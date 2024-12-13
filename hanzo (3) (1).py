import random

def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

def find_primitive_root(prime):
    for candidate in range(2, prime):
        values = set(pow(candidate, exp, prime) for exp in range(1, prime))
        if len(values) == prime - 1:
            return candidate
    return None

def generate_keys():
    while True:
        prime = random.randint(100, 500)
        if is_prime(prime):
            primitive_root = find_primitive_root(prime)
            if primitive_root:
                secret_key = random.randint(1, prime - 2)
                public_key = (prime, primitive_root, pow(primitive_root, secret_key, prime))
                return public_key, secret_key

def encrypt_message(public_key, message):
    prime, root, public_val = public_key
    temp_key = random.randint(1, prime - 2)
    cipher1 = pow(root, temp_key, prime)
    cipher2 = (message * pow(public_val, temp_key, prime)) % prime
    return cipher1, cipher2

def decrypt_message(private_key, public_key, cipher):
    prime, root, public_val = public_key
    cipher1, cipher2 = cipher
    shared_secret = pow(cipher1, private_key, prime)
    inverse_secret = pow(shared_secret, prime - 2, prime)
    return (cipher2 * inverse_secret) % prime

def main():
    print("Simple ElGamal Encryption System")
    public_key, private_key = generate_keys()
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")

    while True:
        print("\nOptions: 1-Encrypt, 2-Decrypt, 3-Exit")
        option = input("Choose an option: ")

        if option == '1':
            message = int(input("Enter a message (integer): "))
            cipher = encrypt_message(public_key, message)
            print(f"Encrypted Message: {cipher}")

        elif option == '2':
            cipher1 = int(input("Enter cipher part 1: "))
            cipher2 = int(input("Enter cipher part 2: "))
            cipher = (cipher1, cipher2)
            original_message = decrypt_message(private_key, public_key, cipher)
            print(f"Decrypted Message: {original_message}")

        elif option == '3':
            print("Exiting...")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
