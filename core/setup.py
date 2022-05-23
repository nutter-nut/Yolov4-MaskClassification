import pip

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', 'opencv-python==4.1.1.26'])
        pip.main(['install', 'lxml'])
        pip.main(['install', 'tqdm'])
        pip.main(['install', 'tensorflow==2.6.2'])
        pip.main(['install', 'absl-py'])
        pip.main(['install', 'easydict'])
        pip.main(['install', 'matplotlib'])
        pip.main(['install', 'pillow'])
        pip.main(['install', 'pytesseract'])
        pip.main(['install', 'pygame'])
        pip.main(['install', 'openpyxl'])
        pip.main(['install', 'pandas'])
        pip.main(['install', 'mysql-connector'])  
    else:
        print("install error")

# Example
if __name__ == '__main__':
    install('argh')