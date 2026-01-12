double_evens(Numbers, Result) :-
    include(even, Numbers, Evens),
    maplist(double, Evens, Result).

even(N) :- 0 is N mod 2.
double(N, D) :- D is N * 2.
