import io
import sys

import six
try:
    from nose.plugins import Plugin
    from nose.plugins.capture import Capture
except ImportError:
    pass
else:

    import nose.plugins.xunit
    from allura.lib.helpers import monkeypatch


    # from https://github.com/asottile/behave/commit/384b028018996728318c508d5acb702c92e81a95
    class CaptureIO(io.TextIOWrapper):
        def __init__(self):
            super().__init__(
                io.BytesIO(),
                encoding='UTF-8', newline='', write_through=True,
            )

        def getvalue(self):
            return self.buffer.getvalue().decode('UTF-8')


    class MonkeyPatchCapture(Plugin):
        """
        This doesn't do anything as a plugin itself.
        It is used to hook into nose execution very early, before the default "capture" plugin starts
        We replace its start() method which uses StringIO and suffers from:
            AttributeError: '_io.StringIO' object has no attribute 'buffer'
            https://github.com/nose-devs/nose/issues/1098
            due to mercurial accessing sys.stdout.buffer which normal python3 stdout has
        This new version uses a CaptureIO class which includes a .buffer attr

        It also replaces the "xunit" plugin's stdout/stderr capturing methods to support .buffer attr
        """
        enabled = False

        def __init__(self):
            super().__init__()

            @monkeypatch(Capture)
            def start(self):
                self.stdout.append(sys.stdout)
                self._buf = CaptureIO()
                sys.stdout = self._buf

            @monkeypatch(nose.plugins.xunit.Xunit)
            def _startCapture(self):
                self._capture_stack.append((sys.stdout, sys.stderr))
                self._currentStdout = CaptureIO()
                self._currentStderr = CaptureIO()
                sys.stdout = TeeInclBuffer(self.encoding, self._currentStdout, sys.stdout)
                sys.stderr = TeeInclBuffer(self.encoding, self._currentStderr, sys.stderr)

            class TeeInclBuffer(nose.plugins.xunit.Tee):
                # add support for .buffer attr to the Tee wrapper
                def __init__(self, *a, **kw):
                    super().__init__(*a, **kw)
                    self.buffer = TeedBuffer([stream.buffer for stream in self._streams])

            class TeedBuffer():
                # wrap multiple output buffers, like Tee does for the higher-level outputs
                # matches io.BufferedWriter signature (partially)
                def __init__(self, buffers):
                    self.buffers = buffers

                def write(self, *args, **kwargs):
                    for buf in self.buffers:
                        buf.write(*args, **kwargs)

                def flush(self):
                    for b in self.buffers:
                        b.flush()
