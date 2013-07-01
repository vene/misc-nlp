for N in 1 10 50 100 500
do
    for S in syl nosyl
    do
        echo "N=${N}..."
        crfsuite learn -a pa -p max_iterations=${N} -g 3 -x stress_${S}_2.txt > log.${N}.${S}_2.txt
    done
done
