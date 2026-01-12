fizzbuzz(N) :-
    ( 0 is N mod 15 -> write('FizzBuzz')
    ; 0 is N mod 3 -> write('Fizz')
    ; 0 is N mod 5 -> write('Buzz')
    ; write(N)
    ), nl.

main :- forall(between(1, 100, N), fizzbuzz(N)).
