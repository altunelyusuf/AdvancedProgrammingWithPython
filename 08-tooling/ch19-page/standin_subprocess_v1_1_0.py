"""Version 1.1.0: sleep no longer blocks inside Popen; poll() answers None until the clock says the child would have ended, and wait(timeout) raises TimeoutExpired as the real module does.
Stand-in for the subprocess module of the chapter 19 page. A browser's Python cannot start processes, so on the page (platform 'emscripten') this module replaces subprocess.run and subprocess.Popen
with a small emulation of exactly what the chapter's examples start: a child Python program given with -c (run in this interpreter, its output and exit code captured, os.kill turned into the
negative return code of the signal), the programs echo, sleep, true and false, and a shell string made of echo commands separated by semicolons. Any other program raises FileNotFoundError as the real
module does for a program that does not exist. It is installed only where real processes are unavailable, and the page says so next to the examples that use it."""
import contextlib, io, os, shlex, signal, subprocess, sys, time, traceback

_real_run, _real_Popen = subprocess.run, subprocess.Popen


class _Exited(BaseException):
    def __init__(self, code):
        self.code = code


class _Signalled(BaseException):
    def __init__(self, sig):
        self.sig = sig


def _child_python(source):
    out, err, code = io.StringIO(), io.StringIO(), 0
    real_kill, real_exit = os.kill, os._exit
    def fake_exit(status):
        raise _Exited(int(status) & 0xFF)
    os._exit = fake_exit
    def fake_kill(pid, sig):
        raise _Signalled(int(sig))
    os.kill = fake_kill
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                exec(compile(source, "<string>", "exec"), {"__name__": "__main__"})
            except SystemExit as e:
                code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
                if e.code is not None and not isinstance(e.code, int):
                    err.write(str(e.code) + "\n")
            except _Exited as x:
                code = x.code
            except _Signalled as s:
                code = -s.sig
            except BaseException:
                traceback.print_exc()
                code = 1
    finally:
        os.kill, os._exit = real_kill, real_exit
    return code, out.getvalue(), err.getvalue()


def _echo(words):
    return 0, " ".join(words) + "\n", ""


def _execute(args, shell):
    if shell:
        lex = shlex.shlex(args, posix=True, punctuation_chars=";")
        lex.whitespace_split = True
        parts, cur = [], []
        for t in lex:
            if t == ";":
                parts.append(cur); cur = []
            else:
                cur.append(t)
        parts.append(cur)
        out = ""
        code = 0
        for p in parts:
            if not p:
                continue
            if p[0] != "echo":
                return 127, out, "%s: command not found\n" % p[0]
            c, o, e = _echo(p[1:]); out += o
        return code, out, ""
    args = [str(a) for a in args]
    prog = args[0]
    if prog == sys.executable and len(args) > 2 and args[1] == "-c":
        return _child_python(args[2])
    if prog == "echo":
        return _echo(args[1:])
    if prog == "sleep":
        return 0, "", ""   # the waiting is done by Popen.wait and Popen.poll against the clock
    if prog == "true":
        return 0, "", ""
    if prog == "false":
        return 1, "", ""
    raise FileNotFoundError(2, "No such file or directory", prog)


def _shape(data, want, text):
    if data is None or not want:
        return None
    return data if text else data.encode()


class Popen:
    def __init__(self, args, stdout=None, stderr=None, shell=False, text=False, universal_newlines=False, **kw):
        self.args, self._shell, self._text = args, shell, bool(text or universal_newlines)
        self._pipe_out, self._pipe_err = stdout == subprocess.PIPE, stderr == subprocess.PIPE
        self._dev_err = stderr == subprocess.DEVNULL
        self.returncode, self._res = None, None
        if not shell:
            prog = str(args[0])
            if prog not in (sys.executable, "echo", "sleep", "true", "false"):
                raise FileNotFoundError(2, "No such file or directory", prog)
        self.pid = 4242
        self._start = time.monotonic()
        self._duration = float(args[1]) if (not shell and str(args[0]) == "sleep") else 0.0

    def _remaining(self):
        return self._start + self._duration - time.monotonic()

    def _finish(self):
        if self._res is None:
            self._res = _execute(self.args, self._shell)
            self.returncode = self._res[0]
            if self._res[1] and not self._pipe_out:
                sys.stdout.write(self._res[1])
        return self.returncode

    def poll(self):
        if self.returncode is None and self._remaining() <= 0:
            self._finish()
        return self.returncode

    def wait(self, timeout=None):
        if self.returncode is None:
            left = self._remaining()
            if timeout is not None and left > timeout:
                time.sleep(timeout)
                raise subprocess.TimeoutExpired(self.args, timeout)
            if left > 0:
                time.sleep(left)
        return self._finish()

    def communicate(self, input=None, timeout=None):
        self.wait(timeout)
        return (_shape(self._res[1], self._pipe_out, self._text), _shape(self._res[2], self._pipe_err, self._text))

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self._finish()


def run(args, *, capture_output=False, stdout=None, stderr=None, text=False, universal_newlines=False, shell=False, check=False, **kw):
    p = Popen(args, stdout=subprocess.PIPE if capture_output else stdout, stderr=subprocess.PIPE if capture_output else stderr, shell=shell, text=text, universal_newlines=universal_newlines)
    so, se = p.communicate()
    if p.returncode and check:
        raise subprocess.CalledProcessError(p.returncode, args, so, se)
    return subprocess.CompletedProcess(args, p.returncode, so, se)


def install():
    if sys.platform == "emscripten":
        subprocess.run, subprocess.Popen = run, Popen
