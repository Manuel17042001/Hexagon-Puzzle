# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_dynamic_libs

z3_binaries = collect_dynamic_libs('z3')

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=z3_binaries,
    datas=[('src/utils/resources', 'resources')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

metadata = {
    'name': 'HexagonPuzzle',
    'description': 'In this puzzle game with hexagonal shapes, your task is to fit all the puzzle pieces into the given pattern. You have to make sure that the yellow hexagons form a coherent island. Work your way through the challenges and skillfully place the shapes to reach the goal!',
    'author': 'Manuel Reichegger',
    'copyright': 'Copyright (c) 2024, Manuel Reichegger',
}

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    **metadata,
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
    icon='src/utils/resources/icon.ico'
)
