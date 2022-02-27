import random
import inspect

for l in inspect.getsourcelines(random.randrange)[0]:
    print(l)


_fp = inspect.getsourcefile(random.randrange)
_fd = os.path.dirname(_fp)
print(_fd) 
os.startfile(_fd)