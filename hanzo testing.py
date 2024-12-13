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

#
#
#

def test_is_prime():
    print("Testing is_prime...")
    assert is_prime(2), "Failed: 2 should be prime."
    assert is_prime(13), "Failed: 13 should be prime."
    assert not is_prime(4), "Failed: 4 should not be prime."
    assert not is_prime(1), "Failed: 1 should not be prime."
    print("All is_prime tests passed.")

def test_find_primitive_root():
    print("Testing find_primitive_root...")
    prime = 7
    primitive_root = find_primitive_root(prime)
    assert primitive_root is not None, "Failed: No primitive root found for 7."
    assert pow(primitive_root, 1, prime) != 1, "Failed: Primitive root must not repeat prematurely."
    print(f"Primitive root {primitive_root} is valid for prime {prime}.")
    print("All find_primitive_root tests passed.")

def test_generate_keys():
    print("Testing generate_keys...")
    public_key, private_key = generate_keys()
    prime, root, public_val = public_key
    assert is_prime(prime), f"Failed: {prime} is not prime."
    assert pow(root, prime - 1, prime) == 1, "Failed: Root must satisfy Fermat's little theorem."
    assert 1 <= private_key < prime - 1, f"Failed: Private key {private_key} is out of range."
    print(f"Keys generated successfully. Public key: {public_key}, Private key: {private_key}.")
    print("All generate_keys tests passed.")

def test_encrypt_decrypt():
    print("Testing encrypt_message and decrypt_message...")
    public_key, private_key = generate_keys()
    original_message = random.randint(1, public_key[0] - 1)
    cipher = encrypt_message(public_key, original_message)
    decrypted_message = decrypt_message(private_key, public_key, cipher)
    assert decrypted_message == original_message, (
        f"Failed: Decrypted message {decrypted_message} does not match original {original_message}."
    )
    print(f"Encryption and decryption successful. Original: {original_message}, Decrypted: {decrypted_message}.")
    print("All encrypt_decrypt tests passed.")

def run_all_tests():
    test_is_prime()
    test_find_primitive_root()
    test_generate_keys()
    test_encrypt_decrypt()
    print("All tests passed successfully!")

if __name__ == "__main__":
    run_all_tests()
