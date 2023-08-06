# ezzthread
Smallest library that every project needs!

It just... Runs your function in new thread with decorator!

```bash
pip install ezzthread
```

# Use
```python
from ezzthread import threaded

@threaded
def func():
    print("Printed from new thread!")
func()
```

