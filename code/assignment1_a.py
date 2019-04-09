import mathlib.utils

for mean, events in [(1,0), (5,10), (3,21), (2.6,40)]:
    print('Poisson(mean:{0:.1f}, events:{1:.0f}) = {2:0.15E}'
           .format(mean, events, mathlib.utils.poisson(mean, events)))
