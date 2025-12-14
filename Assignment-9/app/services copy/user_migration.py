from app.data.users import insert_user

def migrate_users_from_file(filepath="DATA/users.txt"):
    with open(filepath, "r", encoding="utf-8") as file:
        next(file)  

        for line in file:
            line = line.strip()
            if not line:
                continue
            
            username, password_hash, role = line.split(",")

            insert_user(username, password_hash, role)

    print("User migration completed!")
