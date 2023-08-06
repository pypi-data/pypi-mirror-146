from queue import Queue, Empty


class StdinStream:
    def __init__(self, fakeStdin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buf = Queue()
        self.stdin = fakeStdin

    def read(self, n):
        if self.buf.empty():
            for ch in self.stdin.read():
                self.buf.put_nowait(ch)
        buf = []
        for _ in range(n):
            try:
                buf.append(self.buf.get_nowait())
            except Empty:
                break
        return ''.join(buf)

