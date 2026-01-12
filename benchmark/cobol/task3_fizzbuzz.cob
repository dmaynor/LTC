       IDENTIFICATION DIVISION.
       PROGRAM-ID. FIZZBUZZ.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 WS-I PIC 9(3).
       01 WS-MOD3 PIC 9(3).
       01 WS-MOD5 PIC 9(3).
       PROCEDURE DIVISION.
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 100
               DIVIDE WS-I BY 3 GIVING WS-MOD3 REMAINDER WS-MOD3
               DIVIDE WS-I BY 5 GIVING WS-MOD5 REMAINDER WS-MOD5
               EVALUATE TRUE
                   WHEN WS-MOD3 = 0 AND WS-MOD5 = 0
                       DISPLAY "FizzBuzz"
                   WHEN WS-MOD3 = 0
                       DISPLAY "Fizz"
                   WHEN WS-MOD5 = 0
                       DISPLAY "Buzz"
                   WHEN OTHER
                       DISPLAY WS-I
               END-EVALUATE
           END-PERFORM.
           STOP RUN.
