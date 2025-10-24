import modal

image = modal.Image.debian_slim().pip_install("fastapi[standard]")
app = modal.App(name="example-basic-web", image=image)

''' to create a simple endpoint
    @app.function()
    @modal.fastapi_endpoint(
        docs=True  # adds interactive documentation in the browser
    )
    def greet(user: str) -> str:
        return f"Hello {user}!"
'''


''' to create a post URL
{
  "name": "steve"
}
'''
@app.function()
@modal.fastapi_endpoint(method="POST", docs=True)
def goodbye(data: dict) -> str:
    name = data.get("name")
    return f"Goodbye {name}!"