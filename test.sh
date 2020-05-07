#!/bin/sh

TIME=/usr/bin/time

# e.g.
#   cc -DNB_TEST=10 -DEVAL_END=1 -DUSE_SCANF=1 -DUSE_SIZEOF=1 test.c
#   $TIME ./a.out 16384

shuf() { awk 'BEGIN {srand(); OFMT="%.17f"} {print rand(),$0}' | sort -k1,1n | cut -d' ' -f2-; }

for NB_TEST in 1 10
do
    echo "## NB_TEST=$NB_TEST"
    for i in {1..10}
    do
        echo "0 1\n1 0\n0 0\n1 1" | shuf | \
        while read a b
        do
            # compile
            cc -DNB_TEST=$NB_TEST -DEVAL_END=1 -DUSE_SCANF=$a -DUSE_SIZEOF=$b test.c

            # exec
            result=$($TIME ./a.out 16384 2>&1 >/dev/null)

            # e.g. of output: 0 1 elapse: 6.453316 6.45 real 0.54 user 1.96 sys
            echo $a $b $result | awk -v nb_test=$NB_TEST '{
                printf("%d,%d,%.6f,%.2f,%.2f\n",$1,$2,$4,$7/nb_test,$9/nb_test)}'
        done
    done
done
