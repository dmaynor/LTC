#import <Foundation/Foundation.h>

NSArray* doubleEvens(NSArray* numbers) {
    NSMutableArray* result = [NSMutableArray array];
    for (NSNumber* n in numbers) {
        if ([n intValue] % 2 == 0) {
            [result addObject:@([n intValue] * 2)];
        }
    }
    return result;
}
