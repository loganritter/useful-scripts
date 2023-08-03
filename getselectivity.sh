if test ! -f sc; then
    g++ selectivity.cpp -o sc
fi

for temp in 280 310; do
        for pres in `seq 0.01 0.01 0.1`; do

            tail -250 ./$temp/$pres/runlog.log > runlog.tail

            cat runlog.tail | grep "wt_%(Kr)(ME)=" > kr-sorb.tmp
            cat runlog.tail | grep "wt_%(Xe)(ME)=" > xe-sorb.tmp
            cat runlog.tail | grep "Average_N(Kr)=" > kr-sel.tmp
            cat runlog.tail | grep "Average_N(Xe)=" > xe-sel.tmp

            tail -1 kr-sorb.tmp | awk 'END{print '$temp/$pres', ($2*10)/(83.798), ($4*10)/(83.798)}' >> $temp"_AmountSorbed_Kr_mmol_g.dat"
            tail -1 xe-sorb.tmp | awk 'END{print '$temp/$pres', ($2*10)/(131.29), ($4*10)/(131.29)}' >> $temp"_AmountSorbed_Xe_mmol_g.dat"
            tail -1 kr-sel.tmp  | awk 'END{print $2}' > moles_sorbed_Kr.tmp
            tail -1 xe-sel.tmp  | awk 'END{print $2}' > moles_sorbed_Xe.tmp

            ./sc $temp/$pres 20 80 moles_sorbed_Xe.tmp moles_sorbed_Kr.tmp >> $temp"_Selectivity_Xe.dat"
#       ./sc $pres 80 20 moles_sorbed_Kr.tmp moles_sorbed_Xe.tmp >> Selectivity_Kr.dat

            rm *.tmp
            rm runlog.tail
            echo $pres
        done
done
