#bin/bash

base=$(pwd)

for gas in n2; do
        mkdir -p $gas
        cd $gas

        for temp in 77; do
                mkdir -p $temp
                cd $temp

                for pressure in `seq 0.01 0.01 0.09` `seq 0.1 0.1 1.0`; do
                        mkdir -p $pressure
                        cd $pressure
                        cp $base/INPUT.pdb .

                        sed "s/xjobx/$gas"_"$temp"_"$pressure/g" $base/mpmc_submit.sh > mpmc_submit.sh
                        sed "s/xjobx/$gas"_"$temp"_"$pressure/g" $base/mpmc.inp > mpmc.inp
                        #sed -i "s/xtempx/$temp/g" mpmc.inp
                        sed -i "s/xpresx/$pressure/g" mpmc.inp

                        rm -f std*
                        rm -f core.*

                        bsub < mpmc_submit.sh
                        pwd

                        cd ../
                done
                cd ../
        done
        cd ../
done
