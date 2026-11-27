from pathlib import Path
import shutil
try:
    from send2trash import send2trash
except ImportError:
    def send2trash(name):
        # stand-in: move the file to a folder named bin
        Path('bin').mkdir(exist_ok=True)
        shutil.move(name, 'bin')
send2trash('spam/file1.txt')
print('left in spam:', sorted(p.name for p in Path('spam').iterdir()))
print('stand-in bin:', sorted(p.name for p in Path('bin').glob('*')))
