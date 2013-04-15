#for I in 1 5 10 20 50
#do
#    crfsuite learn -a ap -p max_iterations=$I -g 10 -x crf.labeled.3.txt | tee tenfold.3.$I.txt
#    grep -A44 'Iteration #$I' < tenfold.3.$I.txt > tenfold.3.$I.last.txt 
#done

for n in 5 6 # 2 3 4 # 5 6 # 7 8
do
#for c2 in 0.01 0.1 1 10 100
#do
for ps in 0 1
do
for pt in 0 1
do
for iter in 1 5 10 25 50 100
do
#for r in 0.01 0.1 1 10 100
#do
#    crfsuite learn -a arow -p gamma=$r -p feature.possible_states=$ps -p feature.possible_transitions=$pt -p max_iterations=$iter -g 10 -x input/crf.labeled.$n.train | tee arow_logs/ps$ps.pt$pt.$n.$r.$iter

#    crfsuite learn -a lbfgs -p c2=$c2 -p feature.possible_states=$ps -p feature.possible_transitions=$pt -g 10 -x input/crf.labeled.$n.train | tee lbfgs_logs/ps$ps.pt$pt.$n.$c2
#    crfsuite learn -a ap -p max_iterations=$iter -p feature.possible_states=$ps -p feature.possible_transitions=$pt -g 10 -x input/crf.labeled.$n.train | tee ap_logs/ps$ps.pt$pt.$n.$iter
#done
for c in 0.01 0.1 1 10 100
do
    crfsuite learn -a pa -p c=$c -p feature.possible_states=$ps -p feature.possible_transitions=$pt -p max_iterations=$iter -g 10 -x input/crf.labeled.$n.train | tee pa_logs/ps$ps.pt$pt.$n.$c.$iter
done
done
done
done
done
