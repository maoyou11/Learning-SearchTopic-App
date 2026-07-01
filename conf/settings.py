import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, 'db')
DATAS_PATH = os.path.join(DB_PATH, 'datas')
CONFIG_PATH = os.path.join(ROOT_DIR, 'conf')
AUTOHOTKEY_PATH = os.path.join(ROOT_DIR, 'AutoHotkey_2.0.26')
IMAGE_PATH = os.path.join(ROOT_DIR, 'image')


CONF_YAML_PATH = os.path.join(CONFIG_PATH, 'config.yaml')
DATAS_TIKU_PATH = os.path.join(DATAS_PATH, 'tiku.txt')


AHK_EXE = os.path.join(AUTOHOTKEY_PATH, 'AutoHotkey32.exe')
AHK_SCRIPT = os.path.join(AUTOHOTKEY_PATH, 'autoInputText.ahk')


IMAGE_SCREEN_PATH = os.path.join(IMAGE_PATH, 'screen.png')
IMAGE_TITLE_PATH = os.path.join(IMAGE_PATH, 'title.png')
IMAGE_A_PATH = os.path.join(IMAGE_PATH, 'A.png')
IMAGE_B_PATH = os.path.join(IMAGE_PATH, 'B.png')
IMAGE_C_PATH = os.path.join(IMAGE_PATH, 'C.png')
IMAGE_D_PATH = os.path.join(IMAGE_PATH, 'D.png')
IMAGE_NEXT_PATH = os.path.join(IMAGE_PATH, 'next.png')