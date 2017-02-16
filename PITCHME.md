# A niech mnie `__dunder__` świśnie
## O przeciążaniu operatorów w Pythonie

Łukasz Rogalski

# Inspiracja

Raymond Hettinger

*Beyond PEP 8 -- Best practices for beautiful intelligible code*

PyCon 2015

https://youtu.be/wf-BqAjZb8M


# Plan prezentacji
1. Na czym polega przeciążanie, dlaczego warto to robić?
2. Szybki przeglad wraz z przykladami
3. Interesujące przypadki użycia


```
#
3 * [1,2,3] == [1,2,3,1,2,3,1,2,3]

"GDA" in "PyGDA"

(3, 6, 1) > (3, 6, 0)

if obj:
   pass  # ...

with open('pygda.txt', 'w') as f:
    f.write('Hey!')

path = Path()
path2 = Path / 'subdir'
```

- wiele wbudowanych klas (jak i klas w bibliotece standardowej) przeciąża operatory
- czy można zaimplementować klasę dla której będzie można kontrolować przeciążanie?

Oczywiście tak! 😉

# Cel
**pythonic code**: _exploting the features of the Python language to produce code that is clear, concise and maintainable_

```
class Color:
    def __init__(self, r, g, b):
       self.r, self.g, self.b = r, g, b

black = Color (0, 0, 0)
```
class COlor;
    def __init__(self, r, g, b):
       self.r, self.g, self.b = r, g, b

Starting from most common  `__eq__`, `__ne__`

```
class Color:
    def __init__(self, r, g, b):
       self.r, self.g, self.b = r, g, b

black1 = Color(0, 0, 0)
black2 = Color(0, 0, 0)
assert black1 == black2  # AsserionError!
```

```
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

# Co nie jest przeciążalne

## Operator tożsamości (ang. _identity_) - `is`

Dlaczego? Bo tak mówi specyfikacja.

_Every object has an identity, a type and a value. An object’s identity never changes once it has been created; you may think of it as the object’s address in memory. The `is` operator compares the identity of two objects; the `id()` function returns an integer representing its identity._

## Operacje logiczne

`my_obj1 and my_obj2`

### Dlaczego?

Aby wykonać metodę, konieczne jest obliczenie wartości wszystkich argumentów wejściowych. Wykonanie tych argumentów powoduje złamanie zasady leniwego wykonania, która jest zagwarantowana.

- ❌ `a or b`
- ✅ `a | b` (`__or__`)
- ❌ `a and b`
- ✅ `a & b` (`__and__`)

# Interesujące przypadki użycia

Co powinno zwrócić `a < b`?
- `NotImplementedError`
- `True`
- `False`
- Coś innego?

## Numpy: przykład 1
```
import numpy as np
array = np.array(range(10))
# array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
bigger_than_5 = array[array > 5]
bigger_than_5
# array([6, 7, 8, 9])
```
## Numpy: tlumaczenie (1)

- `np.array` przeciąża operator `__gt__`
- wynik działania: macierz wartości typu _boolean_ o tych samych wymiarach co bazowa macierz
- wartości w macierzy: `True` kiedy wartość jest większa niż skalar, inaczej `False`

```
array > 5
# array([False, False, False, False, False, False,  True,  True,  True,  True], dtype=bool)
```

## Numpy: tlumaczenie (2)

- `np.array` przeciąża operator `__getitem__`
- kiedy objekt wewnątrz nawiasów kwadratowych jest macierzą typu _boolean_, zwracany jest podzbiór macierzy wejściowej (z wybrnaymi wierszami i kolumnami)

Wynik: `np.array([6, 7, 8, 9])`

Nieintuicyjny wynik porównania między macierzą i skalaerem pozwolił na uzyskanie prostego i czytelnego API z perspektywy programisty wykorzystującego bibliotekę.


## SQLAlchemy: przykład

```
q = db.Table.query
q = q.filter_by(db.Table.column1 == '123')
q = q.filter_by(sth in db.Table.column2'')
q.first()
```

query object: Select * from Table
.filter_by(sth)
sth := where column 1 == 1

Nieintuicyjny wynik przeciążonej operacji między obiektem reprezentującym kolumnę w tabeli a innym obiektem pozwolił na uzyskanie prostego i czytelnego API z perspektywy programisty wykorzystującego bibliotekę.

# Dzięki!

# Linki
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)
- [R. Hettinger *Beyond PEP 8 -- Best practices for beautiful intelligible code*](https://youtu.be/wf-BqAjZb8M)
- [Slides](github.com/rogalski/pygda22_dunders)
