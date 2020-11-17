def grid(n, radius=1, x0=0, y0=0):
    # attempt to put a uniform x,y grid with n points inside a
    # circle of radius r at (x0,y0).
    # aka more or less the Gauss Circle problem.

    # due to approximation and gridding, some points may be outside radius.

    # https://stackoverflow.com/questions/29330307/how-to-delete-a-set-of-meshgrid-points-inside-a-circle

    import numpy as np
    import math
    # increase N so we get n inside the circle

    N = n * 4/math.pi

    # hand tuned tweak factors when n is small.
    if N<200:
        N*=1.5
    elif N<500:
        N*=1.25
    elif N<1000:
        N*=1.15
    N = math.ceil(N)

    x = np.linspace(-radius, radius, math.ceil(math.sqrt(N)))
    y = np.linspace(-radius, radius, math.ceil(math.sqrt(N)))

    x, y = np.meshgrid(x, y)
    d = np.sqrt((x - x0)**2 + (y - y0)**2)


    # keep n lowest distances., some many by outside the circle.
    pts = list(zip(d.flatten(),x.flatten(),y.flatten()))
    pts.sort(key=lambda x: x[0])

    #return zip(range(1,n+1),zip(*pts[:n+1]))
    d, x, y = zip(*pts[:n+1])
    return zip(range(1,n+1), x, y)
