import bcrypt
import os

USER_DATA_FILE = "users.txt"


def hash_password(plain_text_password):
    pass_bytes = plain_text_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(pass_bytes, salt)
    hashed_str = hashed_pass.decode("utf-8")
    return hashed_str


def PassVerify(plain_text_password, hashed_pass):
    pass_bytes = plain_text_password.encode("utf-8")
    hash_bytes = hashed_pass.encode("utf-8")
    return bcrypt.checkpw(pass_bytes, hash_bytes)


# TEMPORARY TEST CODE -
test_password = "SecurePassword123"

# Test hashing
hashed = hash_password(test_password)
print(f"Original password: {test_password}")
print(f"Hashed password: {hashed}")
print(f"Hash length: {len(hashed)} characters")

# Test verification with correct password
is_valid = PassVerify(test_password, hashed)
print(f"\nVerification with correct password: {is_valid}")

# Test verification with incorrect password
is_invalid = PassVerify("WrongPassword", hashed)
print(f"Verification with incorrect password: {is_invalid}")


def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False
    with open(USER_DATA_FILE, "r") as f:
        for line in f.readlines():
            saved_username, _ = line.strip().split(",", 1)
            if saved_username == username:
                return True
    return False


def register_user(username, password):
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False
    hashed_password = hash_password(password)
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed_password}\n")
    return True


def login_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        return False
    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            saved_username, saved_hashed_password = line.strip().split(",", 1)
            if saved_username == username:
                return PassVerify(password, saved_hashed_password)
    return False


def validate_username(username):
    if len(username) <4:
        return False, "Must be atleast 4 characters or greater"

    if len(username) == 0:
        return False, "Cannot be empty"
    return True,""


def validate_password(password):
    if len(password) <8:
        return False, "Must be atleast 8 characters or greater"
    if len(password) == 0:    
        return False, "Cannot be empty"
    return True,""


def display_menu():
    """Displays the main menu options."""
    print("\n" + "=" * 50)
    print("  MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("   Secure Authentication System")
    print("=" * 50)

    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")

    print("=" * 50)
    choice = input("Enter your choice (1-3): ")
    return choice


def main():
    """Main program loop that processes user input."""
    while True:
        choice = display_menu()

        # Option 1: Registration
        if choice == "1":
            username = input("Enter a username: ")
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print("Error:", error_msg)
                continue

            password = input("Enter a password: ")
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print("Error:", error_msg)
                continue

            register_user(username, password)

        # Option 2: Logging in
        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            if login_user(username, password):
                print("Login successful!")
            else:
                print("Invalid username or password, Login failed.")

        # Option 3: Exit/closing
        elif choice == "3":
            print("Program closing")
            break

        else:
            print("Please enter either 1, 2, or 3 ONLY")


main()
