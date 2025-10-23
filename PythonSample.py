import modal
import sys

# 1. Define the Modal App object. 
# This groups your functions and is the main unit of deployment.
app = modal.App("simple-calculator-app")

# 2. Define the container environment (Image).
# We specify Python 3.11 for the remote container.
remote_image = modal.Image.debian_slim(python_version="3.11")

# 3. Define a remote function.
# The @app.function() decorator tells Modal to run this code in the cloud.
# The 'image' argument attaches our defined Python 3.11 environment.
@app.function(image=remote_image)
def f(i: int):
    # This code executes remotely (in the cloud container)
    if i % 2 == 0:
        print(f"hello: received even number {i}")
        # Standard output (stdout) is streamed back normally
    else:
        # Using sys.stderr can be useful for separating debug/error messages
        print(f"world: received odd number {i}", file=sys.stderr)
    
    # The return value is sent back to the local entrypoint
    return i * i

# 4. Define the local entrypoint.
# This function runs locally when you use 'modal run' and calls the remote function(s).
@app.local_entrypoint()
def main():
    print("--- Starting Local Execution ---")
    
    # Call the remote function 'f' with .remote()
    result_even = f.remote(4)
    result_odd = f.remote(5)
    
    print(f"Local script received result for 4: {result_even}")
    print(f"Local script received result for 5: {result_odd}")
    print("--- Remote Execution Complete ---")
