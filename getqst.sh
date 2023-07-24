#!bin/bash

base=$(pwd)

for gas in c3h4 c3h6; do
        cd $gas

        for temp in 273 298; do
                cd $temp

                echo ""
                echo $gas $temp

                echo "0 0" > $base/$gas"_"$temp"_qst.dat"

                for pres in `seq 0.01 0.01 0.1` `seq 0.2 0.1 1.0`; do
                        cd $pres

                        wtp=$(grep "wt % (ME) =" runlog.log | tail -1 | awk {'print $6'})
                        qst=$(grep "qst =" runlog.log | tail -1 | awk {'print $4'})

                        if [[ $gas == "c3h4" ]]; then
                                cm3=`echo "$wtp * 10 / 40.0639 * 22.4" | bc -l`
                                echo $cm3 $qst >> $base/$gas"_"$temp"_qst.dat"
                                echo $cm3 $qst
                        fi

                        if [[ $gas == "c3h6" ]]; then
                                cm3=`echo "$wtp * 10 / 42.08 * 22.4" | bc -l`
                                echo $cm3 $qst >> $base/$gas"_"$temp"_qst.dat"
                                echo $cm3 $qst
                        fi

                        cd ../
                done

                xstring=$xstring" "$base/$gas"_"$temp"_qst.dat"

                cd ../
        done
        cd ../
done
