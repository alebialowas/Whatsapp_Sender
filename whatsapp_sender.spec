# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['whatsappsender.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('chrome_profile', 'chrome_profile'),
        ('selenium', 'selenium'),
        ('whatsapp_sender.log', '.'),
    ],
    hiddenimports=[
        'selenium',
        'webdriver_manager',
        'pandas',
        'openpyxl'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WhatsAppSender',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True  # Definido como True para mostrar logs no console
)