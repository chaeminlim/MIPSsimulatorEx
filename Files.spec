# -*- mode: python -*-

block_cipher = None


a = Analysis(['Files', '(x86)\\Windows', 'Kits\\10\\Redist\\ucrt\\DLLs\\x64:C:\\Users\\Chaemin', 'Lim\\PycharmProjects\\guiProgramming\\venv\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'GUI.py'],
             pathex=['C:\\Program', 'C:\\Users\\Chaemin Lim\\PycharmProjects\\guiProgramming'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Files',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
