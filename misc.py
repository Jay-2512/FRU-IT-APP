import os


class Misc:
    def hr():
        term_size = os.get_terminal_size()
        for i in range(0, term_size[0]):
            print('-', end='')
        print()