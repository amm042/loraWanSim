"""
https://stackoverflow.com/questions/28567166/uniformly-distribute-x-points-inside-a-circle

H. Vogel, "A Better Way to Construct the Sunflower Head," Mathematical Biosciences, 44(3–4), 1979 pp. 179–189. doi:10.1016/0025-5564(79)90080-4.


function sunflower(n, alpha)   %  example: n=500, alpha=2
    clf
    hold on
    b = round(alpha*sqrt(n));      % number of boundary points
    phi = (sqrt(5)+1)/2;           % golden ratio
    for k=1:n
        r = radius(k,n,b);
        theta = 2*pi*k/phi^2;
        plot(r*cos(theta), r*sin(theta), 'r*');
    end
end

function r = radius(k,n,b)
    if k>n-b
        r = 1;            % put on the boundary
    else
        r = sqrt(k-1/2)/sqrt(n-(b+1)/2);     % apply square root
    end
end

"""
import math
def sunflower(n, alpha=1, radius=1):
    b = round(alpha*math.sqrt(n))
    phi = (math.sqrt(5)+1)/2
    return map(lambda x: sf_pt(x, n, b, radius, phi), range(1,n+1))

def sf_pt(k, n, b, radius, phi):
    if k > n-b:
        r = radius
    else:
        r = radius * math.sqrt(k-1/2)/math.sqrt(n-(b+1)/2)
    theta = 2*math.pi*k/phi**2
    return (k, r*math.cos(theta), r*math.sin(theta))
