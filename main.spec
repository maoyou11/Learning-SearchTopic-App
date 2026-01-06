# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[('api-ms-win-core-sysinfo-l1-2-0.dll', '.')],
    datas=[
        ("ai_deepseek.py", "."),
        ("ai_spark.py", "."),
        ("config.yaml", "."),
        ("config_manager.py", "."),
        ("file_manager.py", "."),
        ("LICENSE", "."),
        ("README.md", "."),
        ("tiku.txt", "."),
        ("ui_ai.py", "."),
        ("ui_main.py", "."),
        ("ui_settings.py", "."),
        ("utils.py", "."),
        ("OCR.py", "."),
    ],
    hiddenimports=['pytesseract','PIL','PIL.Image','pyautogui','tkinter','tkinter.ttk','yaml','sys','os','numpy','ctypes','platform','time','pynput','pynput.keyboard','pynput.mouse', 'pynput', 'pynput.keyboard', 'pynput.mouse',
    'pynput.keyboard._win32', 'pynput.mouse._win32'],
    hookspath=[],
    runtime_hooks=[],
    excludes=['pkg_resources','setuptools','_distutils_hack','distutils'],
    win_no_prefer_redirects=True,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='x86',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)