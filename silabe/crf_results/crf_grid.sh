# for C in 0.1 1.0 10.0 100.0
C=0.01
    for N in 1 2 3 4
    do
        echo "C=${C} N=${N}..."
        crfsuite learn -p c2=${C} -g 3 -x silabe.train.crfsuite.${N}.txt > ${N}grams.C_${C}.cross_val.txt
    done
