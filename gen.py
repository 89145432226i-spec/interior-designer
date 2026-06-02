import os

os.makedirs('templates', exist_ok=True)

with open('templates/project.html', 'w') as f:
    f.write(open('p1.html').read())
    f.write(open('p2.html').read())
    f.write(open('p3.html').read())

with open('templates/client_view.html', 'w') as f:
    f.write(open('cv.html').read())

print("OK!")
for fn in os.listdir('templates'):
    size = os.path.getsize(f'templates/{fn}')
    print(f"  {fn}: {size} bytes")
