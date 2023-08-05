# Tutorial

## Sample data

For the purpose of this, lets generate a test matrix and groups

```python
from mopsy import colsum
import random from rd
# generate a random sparse array with some density
from scipy.sparse import random
mat = random(10, 150, 0.25)

# generate random groups
ngrps = 15
gsets = [x for x in range(15)]
groups = [rd.choice(gsets) for x in range(mat.shape[axis])]
```

## apply a function along an axis

Methods are available to perform `sum`, `median`, `mean` along any axis.

To apply any of these methods

```python
colsum(mat, groups)
```

# Bring your own function

`mopsy` provides a generic `apply` method is also available for perform row-wise or column-wise operations.

lets define our own function to count the number of non-zero elements in the array

```python
import numpy as np

def nz_func(arr):
    return np.count_nonzero(arr)
```

now lets apply the function,

```python
from mopsy import multi_apply

apply(nz_func, mat, axis=1)
```

## Multiple functions

`mopsy` also supports multiple functions. 

```python
from mopsy import multi_apply
import numpy as np

multi_apply([np.sum, np.mean], mat, axis=0)
```

That's all for today! 