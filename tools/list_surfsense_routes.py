from main import app

for route in sorted(app.routes, key=lambda r: getattr(r, "path", "")):
    methods = ",".join(sorted(getattr(route, "methods", []) or []))
    print(f"{methods:24} {getattr(route, 'path', '')}")
