#import <Foundation/Foundation.h>

void countWords(NSString* inputFile, NSString* outputFile) {
    NSString* text = [NSString stringWithContentsOfFile:inputFile encoding:NSUTF8StringEncoding error:nil];
    NSArray* words = [text componentsSeparatedByCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]];

    NSCountedSet* counts = [[NSCountedSet alloc] initWithArray:words];
    NSMutableString* output = [NSMutableString string];

    for (NSString* word in counts) {
        if (word.length > 0) {
            [output appendFormat:@"%@: %lu\n", word, [counts countForObject:word]];
        }
    }

    [output writeToFile:outputFile atomically:YES encoding:NSUTF8StringEncoding error:nil];
}
