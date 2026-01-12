data doubled;
    set numbers;
    if mod(num, 2) = 0;
    doubled = num * 2;
run;
