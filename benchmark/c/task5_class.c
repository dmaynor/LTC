#include <math.h>

typedef struct {
    double x;
    double y;
} Point;

Point point_new(double x, double y) {
    return (Point){x, y};
}

double point_distance_to(Point* self, Point* other) {
    double dx = self->x - other->x;
    double dy = self->y - other->y;
    return sqrt(dx * dx + dy * dy);
}
