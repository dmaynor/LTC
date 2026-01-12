       IDENTIFICATION DIVISION.
       PROGRAM-ID. PARSE-INT.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 WS-INPUT PIC X(20).
       01 WS-OUTPUT PIC S9(9).
       01 WS-SUCCESS PIC 9 VALUE 0.
       01 WS-ERROR PIC X(50).
       PROCEDURE DIVISION.
           MOVE FUNCTION NUMVAL(WS-INPUT) TO WS-OUTPUT
           IF WS-OUTPUT IS NUMERIC
               MOVE 1 TO WS-SUCCESS
           ELSE
               MOVE 0 TO WS-SUCCESS
               MOVE "Invalid integer format" TO WS-ERROR
           END-IF
           STOP RUN.
