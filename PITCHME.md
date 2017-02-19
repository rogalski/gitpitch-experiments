#HSLIDE

# A niech mnie `__dunder__` świśnie
### Przeciążanie operatorów w Pythonie
Łukasz Rogalski

#HSLIDE
## (Luźna) inspiracja
Raymond Hettinger

*Beyond PEP 8: Best practices for beautiful intelligible code*

PyCon 2015

https://youtu.be/wf-BqAjZb8M

#HSLIDE
## Plan prezentacji
1. Dlaczego warto przeciążać?
2. Demo na przykładzie bardzo prostej klasy
4. Czego nie można przeciążyć i dlaczego?
5. Interesujące przypadki użycia

#HSLIDE
```python
3 * [1, 2, 3] == [1, 2, 3, 1, 2, 3, 1, 2, 3]

"GDA" in "PyGDA"

(3, 6, 1) > (3, 6, 0)

path = Path()
path2 = Path / 'subdir'

if obj:
   pass  # ...

with open('pygda.txt', 'w') as f:
    f.write('Hey!')
```

#HSLIDE
- wiele wbudowanych klas (i klas w bibliotece standardowej) przeciąża operatory
- czy można zaimplementować klasę która przeciąży operator zgodnie z naszymi potrzebami?

Oczywiście tak! 😉

#HSLIDE
## Cel
**pythonic**

_exploting the features of the Python language to produce code that is clear, concise and maintainable_

#HSLIDE
## Spójrzmy na trochę kodu :)

#HSLIDE
### Minimalna definicja klasy
```python
class Color:
    def __init__(self, r, g, b):
       self.r, self.g, self.b = r, g, b

black = Color(0, 0, 0)
white = Color(255, 255, 255)
print(black)  # <__main__.Color object at (...)>
print([black, white])  # [<__main__.Color object at (...)>,
                       #  <__main__.Color object at (...)>]
```
## 😞

#HSLIDE
```python
class Color:
    def __init__(self, r, g, b):
       self.r, self.g, self.b = r, g, b
    def __str__(self):
        return "#{:02X}{:02X}{:02X}".format(self.r, self.g, self.b)
    def __repr__(self):
        return "Color({}, {}, {})".format(self.r, self.g, self.b)

black = Color(0, 0, 0)
white = Color(255, 255, 255)
print('Color:', black)  # Color: #000000
print([black, white])  # [Color(0, 0, 0), Color(255, 255, 255)]
```

#HSLIDE
### Jednoargumentowe przeciążalne operatory
| __dunder__  | operacje |
| ------------- | ------------- |
| `object.__str__`  | `str(object)`  |
| `object.__repr__`  | `repr(object)`  |
| `object.__bool__` | `if object: pass`
| `object.__len__` | `len(object)`
| `object.__neg__(self)` | `-object` |
| `object.__pos__(self)` | `+object` |
| `object.__abs__(self)` | `abs(object)` |
| `object.__invert__(self)` | `~object` |
| `object.__complex__(self)` | `complex(object)` |
| `object.__int__(self)` | `int(object)` |
| `object.__float__(self)` | `float(object)` |
| `object.__round__(self[, n])` | `float(object[, n])` |

#HSLIDE
### Operatory dwuargumentowe
```python
class Color:
    def __init__(self, r, g, b):
       self.r, self.g, self.b = r, g, b

black1 = Color(0, 0, 0)
black2 = Color(0, 0, 0)
assert black1 == black2  # AssertionError!
```

#HSLIDE
```python
class Color:
    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b
    def __eq__(self, other):
        return (
            self.r == other.r and
            self.g == other.g and
            self.b == other.b
        )

black1 = Color(0, 0, 0)
black2 = Color(0, 0, 0)
assert black1 == black2
```
#HSLIDE
```python
class Color:
    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b
    def __add__(self, other):
        return type(self)(
            min(self.r + other.r, 255),
            min(self.g + other.g, 255),
            min(self.b + other.b, 255)
        )

red, green = Color(255, 0, 0), Color(0, 255, 0)
blue, white = Color(0, 0, 255), Color(255, 255, 255)
assert red + green + blue == white
```
#HSLIDE
### Lista operatorów dwuargumentowych

#HSLIDE
## Typowe idiomy

#HSLIDE
### Sekwencja
```python
class Color:
    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b
    def __len__(self):
        return 3
    def __getitem__(self, index):
        if index > 2: raise IndexError
        elif index == 0: return self.r
        elif index == 1: return self.g
        else: return self.b

color = Color(0, 127, 255)
assert len(color) == 3
r, g, b = color
assert r == 0
assert g == 127
assert b == 255
```
#HSLIDE
### Mapa
```python
class Color:
    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b
    def __len__(self):
        return 3
    def __getitem__(self, key):
        if key not in {'r', 'g', 'b'}:
            raise KeyError(key)
        return getattr(self, key)

color = Color(0, 127, 255)
assert len(color) == 3
assert color['r'] == 0
assert color['g'] == 127
assert color['b'] == 255
```
#HSLIDE
### Context manager
(...)

#HSLIDE
## Co nie jest przeciążalne?

#HSLIDE
### Operator `is`

**Dlaczego?** Bo tak mówi specyfikacja.

_Every object has an identity, a type and a value. An object’s identity never changes once it has been created; you may think of it as the object’s address in memory. The `is` operator compares the identity of two objects; the `id()` function returns an integer representing its identity._
#HSLIDE

### Operacje logiczne

`my_obj1 and my_obj2`

**Dlaczego?**
Aby wykonać metodę trzeba obliczyć wartości wszystkich argumentów wejściowych, co łamałoby zasadę _leniwego wykonania_ wyrażenia logicznego.

- ☒    `a or b`
- ☑    `a | b`     (dunder: `__or__`)
- ☒     `a and b`
- ☑     `a & b`     (dunder: `__and__`)

#HSLIDE
## Ciekawe przypadki

Co powinno zwrócić `a < b`?
- `NotImplementedError`
- `True`
- `False`
- Coś innego?

#HSLIDE
## Numpy: przykład
```python
import numpy as np
array = np.array(range(10))
# array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
bigger_than_5 = array[array > 5]
bigger_than_5
# array([6, 7, 8, 9])
```

#HSLIDE
## Numpy: analiza

- `np.array` przeciąża operator `__gt__`
- wynik działania: macierz wartości typu _boolean_ o tych samych wymiarach co bazowa macierz
- wartości w macierzy: `True` kiedy wartość jest większa niż skalar, w innym wypadku `False`

```python
array > 5 # array([False, False, False, False, False, False,  
          #        True,  True,  True,  True], dtype=bool)
```

#HSLIDE
### Numpy: analiza

- `np.array` przeciąża operator `__getitem__`
- kiedy obiekt wewnątrz nawiasów kwadratowych jest macierzą typu _boolean_, zwracany jest podzbiór macierzy wejściowej (z wybranymi wierszami i kolumnami)

```python
array = np.array(range(10))
assert array[array > 5] == np.array([6, 7, 8, 9])
```

#HSLIDE
Nieintuicyjny wynik porównania między macierzą a **skalarem** pozwolił na uzyskanie prostego i czytelnego API z perspektywy programisty wykorzystującego bibliotekę.

#HSLIDE
## SQLAlchemy: przykład
#HSLIDE
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)
```
#HSLIDE
## SQLAlchemy: przykład
```python
session = Session()  # object representing DB session

session.add_all([
    User(name='ed', fullname='Ed Jones', password='edspassword'),
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')
])
session.commit()
```
#HSLIDE
## SQLAlchemy: przykład
```python
users = session.query(User).filter(User.name == 'fred').all()
print(users)
# [<User(name='fred', fullname='Fred Flinstone', password='blah')>]
```

#HSLIDE
## SQLAlchemy: analiza
```python
my_query = session.query(User)
# repr: <sqlalchemy.orm.query.Query object at (...)>
# str: SELECT users.id AS users_id, (...) FROM users

my_filter = User.name == 'fred'
# repr: <sqlalchemy.sql.elements.BinaryExpression object at (...)>
# str: users.name = :name_1

filtered_query = my_query.filter(my_filter)
# repr: <sqlalchemy.orm.query.Query object at (...)>
# str: SELECT users.id AS users_id, (...) FROM users WHERE users.name = ?

filtered_users = filtered_query.all()
# [<User(name='fred', fullname='Fred Flinstone', password='blah')>]
```

#HSLIDE
Nieintuicyjny wynik przeciążonej operacji między **obiektem reprezentującym kolumnę w tabeli** a **innym obiektem** pozwolił na uzyskanie prostego i czytelnego API z perspektywy programisty wykorzystującego bibliotekę.

#HSLIDE
# Dzięki!

#HSLIDE
# Linki
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)
- [R. Hettinger *Beyond PEP 8 -- Best practices for beautiful intelligible code*](https://youtu.be/wf-BqAjZb8M)
- [Slides](github.com/rogalski/pygda22_dunders)
