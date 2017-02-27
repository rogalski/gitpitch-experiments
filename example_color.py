class Color:
    def __init__(self, r, g, b):
       self.r, self.g, self.b = r, g, b
    def __str__(self):
        return "#{:02X}{:02X}{:02X}".format(self.r, self.g, self.b)
    def __repr__(self):
        return "Color({}, {}, {})".format(self.r, self.g, self.b)
    def __eq__(self, other):
        return (
            self.r == other.r and
            self.g == other.g and
            self.b == other.b
        )
    def __add__(self, other):
        return type(self)(
            min(self.r + other.r, 255),
            min(self.g + other.g, 255),
            min(self.b + other.b, 255)
        )
    def __getitem__(self, index):
        if isinstance(index, int):
            return self._getitem_index(index)
        else:
            return self._getitem_key(index)
    def _getitem_index(self, index):
        if index > 2:
            raise IndexError(index)
        elif index == 0:
            return self.r
        elif index == 1:
            return self.g
        else:
            return self.b
    def _getitem_key(self, key):
        if key not in {'r', 'g', 'b'}:
            raise KeyError(key)
        return getattr(self, key)

# str, repr
black = Color(0, 0, 0)
white = Color(255, 255, 255)
print('Color:', black)  # Color: #000000
print([black, white])  # [Color(0, 0, 0), Color(255, 255, 255)]

# eq
black1 = Color(0, 0, 0)
black2 = Color(0, 0, 0)
assert black1 == black2

# add
red, green = Color(255, 0, 0), Color(0, 255, 0)
blue, white = Color(0, 0, 255), Color(255, 255, 255)
assert red + green + blue == white

# sequence, almost tuple
color = Color(0, 127, 255)
assert len(color) == 3
assert color[0] == 0
assert color[1] == 127
assert color[2] == 255
r, g, b = color
assert r == 0
assert g == 127
assert b == 255
for component in color:
    print(component, end=" ")  # 0 127 255

# map, almost dict
color = Color(0, 127, 255)
assert color['r'] == 0
assert color['g'] == 127
assert color['b'] == 255
