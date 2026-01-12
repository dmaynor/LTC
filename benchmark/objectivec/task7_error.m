#import <Foundation/Foundation.h>

NSDictionary* parseInt(NSString* s) {
    NSScanner* scanner = [NSScanner scannerWithString:s];
    int value;
    if ([scanner scanInt:&value] && [scanner isAtEnd]) {
        return @{@"success": @YES, @"value": @(value)};
    }
    return @{@"success": @NO, @"error": @"Invalid integer format"};
}
