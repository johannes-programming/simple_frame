import na_quantors as _na

class _Empty:
    pass

class Frame:
    @classmethod
    def _fieldname(cls, value, /):
        return str(value)
    @property
    def width(self):
        return len(self._data)
    @property
    def height(self):
        return self._height
    def set_height(self, value, default=None):
        value = int(value)
        if value < 0:
            raise ValueError
        for f, l in self._data.items():
            while len(l) > value:
                l.pop(-1)
            while len(l) < value:
                l.append(default)
        self._height = value
    def _proon(self, elements, default=None):
        elements = list(elements)
        diff = self.height - len(elements) 
        if diff > 0:
            elements += [default] * diff
        if diff < 0:
            elements = elements[:diff]
        return elements
    def __init__(data={}, default=None):
        self._data = dict()
        self._height = 0
        data = {str(f):list(l) for f, l in data.items()}
        for f, l in data.items():
            self.set_height(max(self.height, len(l)))
        for f, l in data.items():
            self.set_column(fieldname=f, elements=l, default=default)
    def set_column(self, fieldname, elements, default):
        fieldname = str(fieldname)
        elements = list(elements)
        elements = self._proon(elements=elements, default=default)
        self._data[fieldname] = elements







    @property
    def fieldnames(self):
        return list(self._data.keys())






    # key parsing
    def _rawkeypair(self, key):
        if type(key) is tuple:
            return key
        if key is None:
            return (None, None)
        if type(key) is str:
            return (key, None)
        if type(key) is int:
            return (None, key)
        if type(key) is slice:
            return (None, key)
        if type(key) is list:
            if all((type(x) is str) for x in key):
                return (key, None)
            else:
                return (None, key)
        raise TypeError
    def _keypair(self, key):
        xkey, ykey = self._rawkeypair(key)
        ykey = self._ykey(ykey)
        return (xkey, ykey)
    def _ykey(self, key):
        if key is None:
            return list(range(self.height))
        if type(key) is int:
            return key
        if type(key) is slice:
            return self._list_by_slice(key)
        if type(key) is list:
            ans = list()
            for k in key:
                ans += self._list_by_listitem(k)
            return ans
        raise TypeError
    def _list_by_listitem(self, item):
        if type(item) is int:
            return [item]
        if type(item) is slice:
            return self._list_by_slice(item)
        raise TypeError
    def _list_by_slice(self, key):
        indeces = list(range(self.height))
        indeces = indeces[key]
        return indeces











    def __delitem__(self, key):
        self.delitem(*self._keypair(key))
    def __getitem__(self, key):
        return self.getitem(*self._keypair(key))
    def __setitem__(self, key, value):
        self.setitem(*self._keypair(key))

    def delitem(self, xkey, ykey):
        self.delx(xkey)
        self.dely(ykey)
    def dely(self, key):
        if type(key) is int:
            key = [key]
        if type(key) is list:
            key = [int(x) for x in key]
            key.sort(reverse=True)
            for i in key:
                for f in self.fieldnames:
                    self._data[f].pop(i)
        raise TypeError
    def delx(self, key):
        if key is None:
            self._data.clear()
            return
        if type(key) is str:
            self._data.pop(key)
            return
        if type(key) is list:
            for f in key:
                self._data.pop(f)
            return
        raise TypeError

    def getitem(self, xkey, ykey):
        cls = type(self)
        if xkey is None:
            if type(ykey) is int:
                return {f:l[ykey] for f, l in self._data.items()}
            if type(ykey) is list:
                return cls({f:[self._data[i] for i in ykey]})
        elif type(xkey) is str:
            if type(ykey) is int:
                return self._data[xkey][ykey]
            if type(ykey) is list:
                return [self._data[xkey][i] for i in ykey]
        elif type(xkey) is list:
            if type(ykey) is int:
                return [self._data[f][ykey] for f in xkey]
            if type(ykey) is list:
                return [[self._data[f][i] for f in xkey] for i in ykey]
        raise TypeError
    def setitem(self, xkey, ykey, value):
        cls = type(self)
        if xkey is None:
            if type(ykey) is int:
                self.updaterow(index=ykey, update=value)
                return
            if type(ykey) is list:
                raise NotImplementedError
        if type(xkey) is str:
            if type(ykey) is int:
                self.setelem(fieldname=xkey, index=ykey, value=value)
                return
            if type(ykey) is list:
                self.setcolumnelems(fieldname=xkey, indeces=ykey, values=value)
                return
        if type(xkey) is list:
            if type(ykey) is int:
                self.setrowelements(fieldnames=xkey, index=ykey, values=value)
                return
            if type(ykey) is list:
                self.setblock(fieldnames=xkey, indeces=ykey, data=value)
                return
        raise TypeError
    def setblock(self, fieldnames, indeces, data):
        cls = type(self)
        data = cls(data).data
        newrows = [row.to_dict() for i, row in data.iterrows()]
        indeces = list(indeces)
        length = max(len(indeces), len(newrows))
        for n in range(length):
            self.updaterow(
                index=indeces[n],
                update=newrows[n],
            )
    def setcolumnelems(self, fieldname, indeces, values):
        indeces = list(indeces)
        values = list(values)
        length = max(len(indeces), len(values))
        for n in range(length):
            self.setelem(
                fieldname=fieldname, 
                index=indeces[n], 
                value=values[n],
            )
    def setrowelems(self, fieldnames, index, values):
        fieldnames = list(fieldnames)
        values = list(values)
        length = max(len(fieldnames), len(values))
        for n in range(length):
            self.setelem(
                fieldname=fieldnames[n], 
                index=index, 
                value=values[n],
            )
    def updaterow(self, index, update):
        update = dict(update)
        for fieldname, value in update.items():
            self.setelem(
                fieldname=fieldname, 
                index=index, 
                value=value,
            )
    def setelem(self, fieldname, index, value):
        if type(fieldname) is not str:
            raise TypeError
        if fieldname not in self.fieldnames:
            raise KeyError
        if type(index) is not int:
            raise TypeError
        if (index < 0) or (index >= self.height):
            raise IndexError
        self._data.at[index, fieldname] = str(value)
    