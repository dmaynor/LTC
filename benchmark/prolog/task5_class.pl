point(X, Y, point(X, Y)).

distance_to(point(X1, Y1), point(X2, Y2), D) :-
    DX is X1 - X2,
    DY is Y1 - Y2,
    D is sqrt(DX * DX + DY * DY).
