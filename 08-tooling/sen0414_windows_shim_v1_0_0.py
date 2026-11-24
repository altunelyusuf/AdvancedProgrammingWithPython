# Windows display shim (prototype 1.0.0): makes pathlib.Path show Windows form (C:\ drive, backslashes, WindowsPath) while files stay on the real system. Chapters 10 and 11 hidden set-up.
import os, sys, pathlib, tempfile
_P = pathlib.PosixPath
_DRIVE = 'C:'
def _show(p):
    s = _P.__str__(p)
    if s.startswith('/'):
        s = _DRIVE + s
    return s.replace('/', '\\')
class WindowsPath(_P):
    def __str__(self): return _show(self)
    def __repr__(self): return "WindowsPath(%r)" % _show(self).replace('\\','/') if False else "WindowsPath(%s)" % repr(_show(self).replace('\\','/'))
    def __fspath__(self): return _P.__str__(self)
    def with_segments(self, *a): return type(self)(*a)
pathlib.Path = WindowsPath
pathlib.WindowsPath = WindowsPath
