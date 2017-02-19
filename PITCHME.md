#HSLIDE

# A niech mnie `__dunder__` świśnie
### Przeciążanie operatorów w Pythonie
Łukasz Rogalski

#HSLIDE
## Inspiracja
Raymond Hettinger

*Beyond PEP 8: Best practices for beautiful intelligible code*

PyCon 2015

https://youtu.be/wf-BqAjZb8M

#HSLIDE
## Plan prezentacji
1. Na czym polega przeciążanie
2. Dlaczego warto przeciążać?
3. Przykłady
4. Czego nie można przeciążyć i dlaczego?
5. Interesujące przypadki użycia

#HSLIDE
```python
3 * [1,2,3] == [1,2,3,1,2,3,1,2,3]

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
# Spójrzmy na trochę kodu :)

#HSLIDE
## Minimalna definicja klasy
```python
class Color:
    def __init__(self, r, g, b):
       self.r, self.g, self.b = r, g, b

black = Color(0, 0, 0)
white = Color(0xFF, 0xFF, 0xFF)
print(black)  # <__main__.Color object at (...)>
print([black, white]])  # [<__main__.Color object at (...)>,
                        #  <__main__.Color object at (...)>]
```
### 😞

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
white = Color(0xFF, 0xFF, 0xFF)
print(black)  # #000000
print([black, white]])  # [Color(0, 0, 0), Color(255, 255, 255)]
```

#HSLIDE
## Przykładowe jednoargumentowe przeciążalne operatory
- `object.__str__` - `str(object)`
- `object.__repr__` - `repr(object)`
- `object.__bool__` - `if object: pass`

- `object.__neg__(self)` - `-object`
- `object.__pos__(self)` - `+object`
- `object.__abs__(self)` - `abs(object)`
- `object.__invert__(self)` - `~object`

- `object.__complex__(self)` - `complex(object)`
- `object.__int__(self)` - `int(object)`
- `object.__float__(self)` - `float(object)`
- `object.__round__(self[, n])` - `float(object[, n])`
(...)

#HSLIDE
## Operatory dwuargumentowe - `__eq__`
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
## Operatory dwuargumentowe - `__add__`
```python
class Color:
    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b
    def __add__(self, other):
        return type(self)(
            self.r + other.r,
            self.g + other.g,
            self.b + other.b
        )

red = Color(0xFF, 0, 0)
green = Color(0, 0xFF, 0)
blue = Color(0, 0, 0xFF)
white = Color(0xFF, 0xFF, 0xFF)
assert red + green + blue == white
```
#HSLIDE
# Lista operatorów dwuargumentowych

#HSLIDE
# Typowe idiomy
Klasa iterowalna

#HSLIDE

## Co nie jest przeciążalne?
#HSLIDE

### Operator tożsamości (ang. _identity_) - `is`

**Dlaczego?** Bo tak mówi specyfikacja.

_Every object has an identity, a type and a value. An object’s identity never changes once it has been created; you may think of it as the object’s address in memory. The `is` operator compares the identity of two objects; the `id()` function returns an integer representing its identity._
#HSLIDE

### Operacje logiczne

`my_obj1 and my_obj2`

**Dlaczego?** Aby wykonać metodę, konieczne jest obliczenie wartości wszystkich argumentów wejściowych, co łamałoby zasadę leniwego wykonania wyrażenia logicznego.

- ❌     `a or b`
- ✅     `a | b`     (dunder: `__or__`)
- ❌     `a and b`
- ✅     `a & b`     (dunder: `__and__`)

#HSLIDE
## Interesujące przypadki użycia

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
Nieintuicyjny wynik porównania między macierzą i skalaerem pozwolił na uzyskanie prostego i czytelnego API z perspektywy programisty wykorzystującego bibliotekę.

#HSLIDE
## SQLAlchemy: przykład

```python
q = db.Table.query
q = q.filter_by(db.Table.column1 == '123')
q = q.filter_by(sth in db.Table.column2'')
q.first()
```

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
```python
users = session.query(User).filter(User.name == 'fred').all()
print(users)
# [<User(name='fred', fullname='Fred Flinstone', password='blah')>]
```

#HSLIDE
## SQLAlchemy: analiza
```python
my_query = session.query(User)  # <sqlalchemy.orm.query.Query object at (...)>
# SELECT users.id AS users_id, (...) FROM users

my_filter = User.name == 'fred' # <sqlalchemy.sql.elements.BinaryExpression object at (...)>
# users.name = :name_1

filtered_query = my_query.filter(my_filter)  # <sqlalchemy.orm.query.Query object at (...)>
# SELECT users.id AS users_id, (...) FROM users WHERE users.name = ?

filtered_users = filtered_query.all()
# [<User(name='fred', fullname='Fred Flinstone', password='blah')>]
```

#HSLIDE
Nieintuicyjny wynik przeciążonej operacji między obiektem reprezentującym kolumnę w tabeli a innym obiektem pozwolił na uzyskanie prostego i czytelnego API z perspektywy programisty wykorzystującego bibliotekę.

#HSLIDE
# Dzięki!

#HSLIDE
# Linki
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)
- [R. Hettinger *Beyond PEP 8 -- Best practices for beautiful intelligible code*](https://youtu.be/wf-BqAjZb8M)
- [Slides](github.com/rogalski/pygda22_dunders)
