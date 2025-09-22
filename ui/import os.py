import os

server = "kakapo"
shares_to_test = ["USB1", "SomeShare"]  # example shared folders

for share in shares_to_test:
    path = rf"\\{server}\{share}"
    if os.path.exists(path):
        print(f"Accessible: {path}")
    else:
        print(f"Cannot access: {path}")
