for F in ./log*; do
        echo "($F): ["
        cat $F | grep -C10 'Holdout group: 2' | grep '\b1:' | cut -d" " -f11 | cut -c 1-6
        cat $F | grep -C10 'Holdout group: 3' | grep '\b1:' | cut -d" " -f11 | cut -c 1-6
        tail -n10 $F | grep '\b1:' | cut -d" " -f11 | cut -c 1-6
done
