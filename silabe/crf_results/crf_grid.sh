for C in 10.0
do
    for N in 2 3 4
    do
        echo "C=${C} N=${N}..."
        crfsuite learn -p c2=${C} -g 3 -x -l silabe.train.crfsuite.${N}.txt > log.${N}.C=${C}.txt
    done
done
