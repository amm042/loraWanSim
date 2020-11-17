def rand(n, radius=1, seed=None):
    # randomly (uniform) place points not more than
    # radius distance to the origin
    import numpy as np
    from numpy.random import default_rng
    import math
    rng = default_rng(seed)

    def pnt(p, radius):
        # avoid biasing to central points
        # https://mathworld.wolfram.com/DiskPointPicking.html
        r = math.sqrt(radius**2*rng.random())
        theta = 2*math.pi*rng.random()
        return p, r * math.cos(theta), r * math.sin(theta)

    return map(lambda x: pnt(x, radius), range(1,n+1))
