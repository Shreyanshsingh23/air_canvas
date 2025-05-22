# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['air_canvas_tkinter_app.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\\\Program Files\\\\Python310\\\\lib\\\\site-packages\\mediapipe', 'mediapipe'), ('C:\\\\Program Files\\\\Python310\\\\lib\\\\site-packages\\cv2', 'cv2')],
    hiddenimports=['PIL', 'PIL._tkinter_finder', 'cv2', 'mediapipe', 'numpy'],
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
    a.binaries,
    a.datas,
    [],
    name='air_canvas_tkinter_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
