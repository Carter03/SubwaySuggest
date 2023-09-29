import os

for img in os.listdir('utils/static/images'):
    name = os.path.basename(img)
    # newName = name[1:].replace(' ', '_')
    os.rename(os.path.join('utils/static/images', name), os.path.join('utils/static/images', f'{name}.jpeg'))