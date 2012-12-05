for N in 2 3 4
do
    for C in 0.01 0.1 1.0 10.0
    do
        F=log.$N.C=$C.txt
        echo "($N, $C): ["
        cat $F | grep -C30 'Holdout group: 2' | grep '0:' | cut -d" " -f11 | cut -c 1-6
        cat $F | grep -C30 'Holdout group: 3' | grep '0:' | cut -d" " -f11 | cut -c 1-6
        tail -n30 $F | grep '0:' | cut -d" " -f11 | cut -c 1-6
    done
done
