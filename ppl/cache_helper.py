import cachetools
import collections


def cache_key(*args, **kwargs):
    """
    Compute key of input values to cache prorogued fn.
    Mutable containers like list, and dictionary are first transformed to frozen set, 
    such that the hash can be computed.
    """
    hashable_args = []
    hashable_kwargs = {}

    for a in args:
        hashable_args.append(freeze(a))

    for k, v in kwargs.items():
        t = freeze(v)
        hashable_kwargs[k] = t

    key = cachetools.keys.hashkey(*hashable_args, **hashable_kwargs)

    return key


def freeze(v):
    """ 
    Return an element representing v which is hashable
    Base case: v is already hashable, the return v.
    Recursion case:
    - v is list: then create a frozenset made of tuples (index, freeze(v[index]))
    - v is a dict: create a frozenset of elements v[key] : freeze(v[key])
    """
    try:
        hash(v)
        return v
    except TypeError:
        if type(v) is list:
            v_index = []
            index = 0
            for e in v:
                v_index.append((index, e))
                index += 1
            return frozenset(list(map(freeze, v_index)))
        elif type(v) is dict:
            return frozenset(list(map(lambda kv: (kv[0], freeze(kv[1])), v.items())))
