#import <Foundation/Foundation.h>

void fetchURL(NSString* urlString, void (^completion)(BOOL success, NSString* body)) {
    NSURL* url = [NSURL URLWithString:urlString];
    NSURLSession* session = [NSURLSession sharedSession];

    [[session dataTaskWithURL:url completionHandler:^(NSData* data, NSURLResponse* response, NSError* error) {
        if (error) {
            completion(NO, error.localizedDescription);
        } else {
            completion(YES, [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding]);
        }
    }] resume];
}
