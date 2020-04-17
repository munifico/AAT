import sys
mod = sys.modules[__name__]
for i in range(10):
    setattr(mod, 'var_{}'.format(i), i)

print(var_0)