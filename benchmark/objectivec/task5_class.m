#import <Foundation/Foundation.h>
#import <math.h>

@interface Point : NSObject
@property double x;
@property double y;
- (instancetype)initWithX:(double)x y:(double)y;
- (double)distanceTo:(Point*)other;
@end

@implementation Point
- (instancetype)initWithX:(double)x y:(double)y {
    self = [super init];
    if (self) {
        _x = x;
        _y = y;
    }
    return self;
}

- (double)distanceTo:(Point*)other {
    double dx = self.x - other.x;
    double dy = self.y - other.y;
    return sqrt(dx * dx + dy * dy);
}
@end
