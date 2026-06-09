import customtkinter
import os
customtkinter_path = os.path.dirname(customtkinter.__file__)

a = Analysis(
    ['src\\main.py'],
    pathex=['src'],
    binaries=[],
    datas=[('assets', 'assets'), (customtkinter_path, 'customtkinter')],
    hiddenimports=['pandas', 'openpyxl', 'controllers', 'views', 'database', 'uvicorn', 'fastapi', 'pywhatkit', 'pydantic', 'services.fast'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='UniGym_Pro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\logo.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='UniGym_Pro',
)
