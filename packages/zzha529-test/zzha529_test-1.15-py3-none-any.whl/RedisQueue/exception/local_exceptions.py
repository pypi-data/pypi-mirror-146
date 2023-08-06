class NumberProcessException(Exception):
    def __init__(self, msg):
        self.msg = str(msg) + ' < 1, cannot make such number of processes!'

    def __str__(self):
        return self.msg
