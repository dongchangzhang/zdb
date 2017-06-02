from .const import *
from string import digits

class Token:
    def __init__(self, input, flag = False):
        self.mark = False
        self.id = None
        self.parent = None
        self.type, self.attribute = self.analysis(input, flag)
        # print("token info", input, self.type, self.attribute)
    def __eq__(self,token):
        return self.type == token.type and self.attribute == token.attribute
    def __str__(self):
        if self.type == TERMINATOR:
            value = KEY_WORDS[self.attribute].upper()
        else:
            value = self.attribute
        return "<%s, %s>" % (self.type, value)
    def is_id(self):
        return self.type == ID
    def is_value(self):
        return self.type == VALUE
    def is_state(self):
        return self.type == STATE
    def is_terminator(self):
        return self.type == TERMINATOR
    def is_end(self):
        return self.type == END_STATE
    def no_use(self):
        if self.type == TERMINATOR and KEY_WORDS[self.attribute] in ['[', ']', '(', ')']:
            return True
        return False
    def equal(self, input):
        if self.type != TERMINATOR:
            return False
        if input.upper() == KEY_WORDS[self.attribute].upper():
            return True
        return False
    def analysis(self, input, flag):
        if input is None:
            if flag:
                return NULL_STATE, None
            return END_STATE, None
        if len(input) == 0:
            return ERROR, ERROR_INPUT
        isdigit = True
        for d in input:
            if d not in digits:
                isdigit = False
                break
        if isdigit:
            return VALUE, input
        for i in range(0, len(KEY_WORDS)):
            if input.upper() == KEY_WORDS[i].upper():
                return TERMINATOR, i
        if not input.startswith(("'", '"')) and not input.endswith(('"', "'")) and input[0] not in digits:
            if flag:
                return STATE, input
            return ID, input
        if len(input) < 2:
            return ERROR, ERROR_INPUT
        if input.startswith("'") and input.endswith("'"):
            return VALUE, input
        if input.startswith('"') and input.endswith('"'):
            return VALUE, input
        return ERROR, ERROR_INPUT
    def mark_it(self):
        self.mark = True
    def have_mark(self):
        return self.mark
    def set_id(self, id):
        self.id = id
    def get_id(self):
        return self.id
    def set_parent(self, parent):
        self.parent = parent
    def get_parent(self):
        return self.parent
    def get_lable(self):
        if self.type == TERMINATOR:
            return KEY_WORDS[self.attribute]
        elif self.type == NULL_STATE:
            return "null"
        else:
            return self.attribute

if __name__ == '__main__':
    token1 = Token(ID, 1)
    token2 = Token(ID, 1)
    print(token1 == token2)
    token1.is_id()