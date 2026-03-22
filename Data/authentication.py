import chromadb
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

client = chromadb.PersistentClient(path="./chroma_db")
users  = client.get_or_create_collection("users")
# client = chromadb.Client()
# users  = client.get_or_create_collection("users")

users.add(
    ids       = ["john"],
    documents = ["User john"],
    metadatas = [{
        "username": "john",
        "password": hash_password("password123")  # ← Hashed!
    }]
)

users.add(
    ids       = ["sarah"],
    documents = ["User sarah"],
    metadatas = [{
        "username": "sarah",
        "password": hash_password("mypass456")  # ← Hashed!
    }]
)


