data Point = Point { x :: Double, y :: Double }

distanceTo :: Point -> Point -> Double
distanceTo p1 p2 = sqrt ((x p2 - x p1)^2 + (y p2 - y p1)^2)
