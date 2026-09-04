import os

base = r"C:\Claude\SteelFraming\Site\public\content"

old_js = "body:new FormData(form),mode:'no-cors'"
new_js = "body:new URLSearchParams(new FormData(form)).toString(),mode:'no-cors',headers:{'Content-Type':'application/x-www-form-urlencoded'}"

changed = []
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fh:
                content = fh.read()
            if old_js in content:
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write(content.replace(old_js, new_js))
                changed.append(path)

print(f"Alterados: {len(changed)}")
for p in changed:
    print(p)