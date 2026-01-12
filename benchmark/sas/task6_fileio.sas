proc freq data=words noprint;
    tables word / out=counts;
run;

data _null_;
    set counts;
    file "output.txt";
    put word ": " count;
run;
