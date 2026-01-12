#include <cmath>

class Point {
public:
    double x, y;

    Point(double x, double y) : x(x), y(y) {}

    double distance_to(const Point& other) const {
        double dx = x - other.x;
        double dy = y - other.y;
        return std::sqrt(dx * dx + dy * dy);
    }
};
