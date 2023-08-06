import os


def size():
    env = os.environ

    if 'LINES' in env and 'COLUMNS' in env:
        cr = env['LINES'], env['COLUMNS']
    else:
        cr = None

    # noinspection PyShadowingNames,PyBroadException,SpellCheckingInspection
    def ioctl_gwinsz(fd):
        try:
            import fcntl
            import termios
            import struct

            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except Exception:
            return
        return cr

    if not cr:
        cr = ioctl_gwinsz(0) or ioctl_gwinsz(1) or ioctl_gwinsz(2)
    if not cr:
        # noinspection PyBroadException
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_gwinsz(fd)
            os.close(fd)
        except Exception:
            cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

    return int(cr[1]), int(cr[0])


columns = size()[0]


rows = size()[1]
