import re
from types import FunctionType
format_lookup = re.compile(r"\${([a-z0-9_+=:;,&!~%@#$^*()\"'<>?.|`\[\]\\-]+)\}", \
                re.IGNORECASE)

class format:
    replacements = {}
    
    def __init__(self, replacements):
        self.replacements = replacements
    
    def replacer(self, val):
        tmp = val.group(1).split(":", 1)
        title = tmp[0]
        repl = self.replacements.get(title, "#{UNDEFINED: "+title+"}")
        if type(repl) == FunctionType:
            args = {}
            if len(tmp) > 1:
                entries = tmp[1].split(";")
                for entry in entries:
                    entry = entry.split("=", 1)
                    if len(entry) > 1:
                        args[entry[0]] = entry[1]
                    else:
                        arg[entry[0]] = True
            return repl(args)
        elif type(repl) == bytes:
            return repl.decode()
        elif type(repl) != str:
            return str(repl)
        else:
            return repl

    def format(self, input):
        return format_lookup.sub(self.replacer, input)
