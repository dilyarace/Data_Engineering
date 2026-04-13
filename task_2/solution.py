import hashlib
import os

# Settings
data_dir = "./task2"       
email = "dilyarace@gmail.com" 

# Step 1: Read only .data files (exactly 256)
files = sorted(f for f in os.listdir(data_dir) if f.endswith(".data"))
print(f"Files found: {len(files)}") 

# Step 2: Calculate the SHA3-256 hash for each file
hashes = []
for fname in files:
    path = os.path.join(data_dir, fname)
    with open(path, "rb") as f:      
        data = f.read()
    h = hashlib.sha3_256(data).hexdigest()
    hashes.append(h)

# Step 3: Sort by product (digit + 1)
def sort_key(h):
    product = 1
    for c in h:
        product *= (int(c, 16) + 1)
    return product

hashes_sorted = sorted(hashes, key=sort_key)

# Step 4: Join without dividers
joined = "".join(hashes_sorted)

# Step 5: Add email to the end
final_str = joined + email

# Step 6: Final SHA3-256
result = hashlib.sha3_256(final_str.encode("utf-8")).hexdigest()
print(f"Ответ: {result}")