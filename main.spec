# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('ui', 'ui'),
        ('ui/Images', 'ui/Images'),
        ('ui/style', 'ui/style'),
        ('ui/abstract', 'ui/abstract'),
        ('logique_metier', 'logique_metier'),
        ('logique_metier/abstract_logic', 'logique_metier/abstract_logic'),
        ('logique_metier/backbone', 'logique_metier/backbone'),
        ('logique_metier/generate', 'logique_metier/generate'),
        ('interface', 'interface')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Video_Processing',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
