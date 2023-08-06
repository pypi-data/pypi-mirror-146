# montocarlo-ol-circlearea
A Python library for calculating Area of overlapped region between 2 Circle using MontoCarlo method (Random Points)

### Installation
```
pip install montocarlo-ol-circlearea
```

### Get started
How to calculate area of overlapped region of the circle with this lib:

```Python
from montocarlo_ol_circlearea import Overlapped_2_circles

# Instantiate a  Overlapped_2_circle object with 3 params c1 ,c2, Random points
   '''
    :param _c1: circle1[center c1, center c2, radius r1]
    :type _c1: list
    :param _c2: circle2[center c1, center c2, radius r2]
    :type _c2: list
    :param _N: Number of Random Points
    :type _N: int
   '''
MonteCarlo = Overlapped_2_circles([0,0,2],[2,2,2],10000)

# Call the area method
result = MonteCarlo.area()
```
# source code link
https://github.com/sabareeswarans11/montocarlo-ol-circlearea