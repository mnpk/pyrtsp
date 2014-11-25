import termcolor

def chunk_string(string, length):
    size = max(len(string), 1)
    return [string[0+i:length+i] for i in range(0, size, length)]

class MessageView:
    def __init__(self, msg_width = 55, view_width = 80, send_color = 'green', recv_color = 'cyan'):
        self.msg_width = msg_width
        self.view_width = view_width
        self.send_color = send_color
        self.recv_color = recv_color

    def __to_lines(self, msg):
        msg = str(msg)
        msg = msg.replace('\r\n', '\n')
        lines = msg.split('\n')
        items = []
        for line in lines:
            for chunk in chunk_string(line, self.msg_width):
                items.append(chunk)
        return items

    def __border(self, width, align):
        border = ' {:s} '.format('-' * (width + 2))
        if not align == 'left':
            border = ' ' * (self.view_width - width) + border
        return border

    def __build_line(self, line, width, align):
        if align == 'left':
            s = (' {:<%ss} '%width).format(line)
        else:
            s = (' {:>%ss} '%width).format(line)
        return s

    def __wrap_line(self, s, width, align, is_final):
        if is_final:
            if align == 'left':
                s = '/' + s + '|'
            else:
                s = '|' + s + '\\'
        else:
            s = '|' + s + '|'
        if not align == 'left':
            s = ' ' * (self.view_width - width) + s
        return s

    def __out(self, msg, align='left', color='green'):
        lines = self.__to_lines(msg)
        width = max([len(s) for s in lines])
        termcolor.cprint(self.__border(width, align), color)
        for i, line in enumerate(lines):
            s = self.__build_line(line, width, align)
            s = self.__wrap_line(s, width, align, (i == len(lines) - 1))
            termcolor.cprint(s, color)
        termcolor.cprint(self.__border(width, align), color)

    def recv(self, msg):
        self.__out(msg, align='left', color=self.recv_color)

    def send(self, msg):
        self.__out(msg, align='right', color=self.send_color)
