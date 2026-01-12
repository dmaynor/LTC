struct Point
    x::Float64
    y::Float64
end

function distance_to(p1::Point, p2::Point)
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    sqrt(dx^2 + dy^2)
end
