#!/bin/sh

# the output expected:
#   real 0.00
#   user 0.00
#   sys 0.00
# e.g.
#   cc -DNB_TEST=10 -DEVAL_END=1 -DUSE_SCANF=1 -DUSE_SIZEOF=1 test.c
#   $TIME ./a.out 16384
TIME="/usr/bin/time -p"

patt() {
    awk '
    BEGIN {
        srand();
        OFMT="%.17f";
        print(rand()" 0 0");
        print(rand()" 0 1");
        print(rand()" 1 0");
        print(rand()" 1 1");
    }' | sort -k1,1n | cut -d' ' -f2-;
}

do_test() {
    if ls result-*.csv >/dev/null 2>&1 ; then
        echo "ERROR: must remove result-*.csv into somewhere before it runs."
        exit 1
    fi

    for nb_test in 1 10
    do
        for eval_point in EVAL_MID EVAL_END
        do
            echo "## NB_TEST=$nb_test" >> result-${eval_point}-${nb_test}.csv
            for i in `seq 1 10`
            do
                echo "testing $nb_test - $eval_point - $i ..."
                patt | while read a b
                do
                    # compile
                    cc -DNB_TEST=$nb_test -D$eval_point \
                        -DUSE_SCANF=$a -DUSE_SIZEOF=$b test.c

                    # exec
                    result=`($TIME ./a.out 16384 2>&1 >/dev/null) | awk '{print}' ORS=" "`

                    # e.g. 0 1 elapse: 6.440249 real 6.45 user 0.53 sys 1.98
                    echo $a $b $result | awk -v nb_test=$nb_test '{
                        printf("%d,%d,%.6f,%.2f,%.2f,%.2f\n",
                            $1,$2,$4,$6/nb_test,$8/nb_test,$10/nb_test)
                        }'
                done >> result-${eval_point}-${nb_test}.csv
            done
        done
    done
}

do_plot() {
    for nb_test in 1 10
    do
        for eval_point in EVAL_MID EVAL_END
        do
            python3 plot.py result-${eval_point}-${nb_test}.csv
        done
    done
}

do_test
#do_plot
