# run_once.py
print("Starting...")
import re
import uuid

with open("Data/data.py", "r") as f:
    content = f.read()

count = 0
while 'str(uuid.uuid4())' in content:
    content = content.replace(
        'str(uuid.uuid4())',
        f'"{str(uuid.uuid4())}"',
        1
    )
    count += 1

with open("Data/data.py", "w") as f:
    f.write(content)

print(f"✅ Fixed {count} IDs in data.py!")