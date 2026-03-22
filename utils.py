import hashlib
from Data.authentication import users , client

print("Initializing users collection with sample data...")
print(f"Existing users in collection: {users.get()}")
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# utils.py
import hashlib
from Data.authentication import users, client

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_login(username, password):
    try:
        # 1. Look up the user
        result = users.get(ids=[username])
        
        # 2. If user doesn't exist, fail
        if not result or not result['ids']:
            print(f"User {username} not found")
            return False
            
        # 3. Get the stored hash from metadata
        stored_hash = result['metadatas'][0]['password']
        
        # 4. Hash the password the user just typed in Streamlit
        provided_hash = hash_password(password)
        
        # 5. Compare them
        if provided_hash == stored_hash:
            print("✅ Login Success!")
            return True
        else:
            print("❌ Password Incorrect")
            return False
            
    except Exception as e:
        print(f"Login error: {e}")
        return False