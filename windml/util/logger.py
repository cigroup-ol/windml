class Logger(object):
    def __init__(self, scope):
        self.logs, self.bindings, self.const_bindings = {}, {}, {}
        self.scope = scope

    def add_const_binding(self, var_name, name):
        self.const_bindings[name] = var_name

    def add_binding(self, var_name, name):
        self.bindings[name] = var_name
        self.logs[name] = []

    def const_log(self):
        for k, v in self.const_bindings.iteritems():
            self.logs[k] = self.scope.__getattribute__(v)

    def log(self):
        for k, v in self.bindings.iteritems():
            self.logs[k].append(self.scope.__getattribute__(v))

    def all(self):
        return self.logs

    def last(self):
        last = {}
        for k in self.logs.keys():
            if(type(self.logs[k]) == list):
                last[k] = self.logs[k][-1]
            else:
                last[k] = self.logs[k]
        return last

