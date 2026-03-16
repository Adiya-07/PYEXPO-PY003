import os

def read_log(path):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    try:
        with open(path, 'rb') as f:
            content = f.read()
        
        # Try different encodings
        for enc in ['utf-16', 'utf-16-le', 'utf-16-be', 'utf-8']:
            try:
                text = content.decode(enc)
                print(f"--- Content of {path} ({enc}) ---")
                print(text[:2000]) # Print first 2000 chars
                return
            except UnicodeDecodeError:
                continue
        print(f"Could not decode {path}")
    except Exception as e:
        print(f"Error reading {path}: {e}")

read_log('startup_error.log')
read_log('output.log')
