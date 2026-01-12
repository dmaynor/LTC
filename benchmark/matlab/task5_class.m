classdef Point
    properties
        x
        y
    end
    methods
        function obj = Point(x, y)
            obj.x = x;
            obj.y = y;
        end
        function d = distance_to(obj, other)
            dx = obj.x - other.x;
            dy = obj.y - other.y;
            d = sqrt(dx^2 + dy^2);
        end
    end
end
