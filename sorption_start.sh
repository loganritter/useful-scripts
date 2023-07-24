#bin/bash

base=$(pwd)

for temp in 290 300; do
        mkdir -p $temp
        cd $temp

        #for pressure in `seq 0.1 0.1 1.0`; do
        for pressure in 0.0003 0.0005 0.0008 0.001 0.002; do
                mkdir -p $pressure
                cd $pressure
                cp $base/LJ_2x2x2.pdb .

                sed "s/xjobx/$temp"_"$pressure/g" $base/mpmc_submit.sh > mpmc_submit.sh
                sed "s/xjobx/$temp"_"$pressure/g" $base/mpmc.inp > mpmc.inp
                sed -i "s/xtempx/$temp/g" mpmc.inp
                sed -i "s/xpresx/$pressure/g" mpmc.inp

                rm -f std*
                rm -f core.*

                bsub < mpmc_submit.sh
                pwd

                cd ../
        done
        cd ../
done
