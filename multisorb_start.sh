#/bin/bash

base=$(pwd)

for gas_pair in c2h2+c2h4 c2h2+c2h6 c2h4+c2h6 co2+c2h2; do
    mkdir -p $gas_pair
    cd $gas_pair
    model=`echo $gas_pair`

    for temp in 273 298; do
        mkdir -p $temp
        cd $temp

        for pressure in `seq 0.01 0.01 0.1` `seq 0.2 0.1 1.0`; do
             mkdir -p $pressure
            cd $pressure

            sed "s/xjobx/$model"_"$temp"_"$pressure/g" $base/mpmc_submit.sh > mpmc_submit.sh
            sed "s/xjobx/$model"_"$temp"_"$pressure/g" $base/mpmc.inp > mpmc.inp

            fug=`echo "scale=3; $pressure / 2.0" | bc`

            sed -i "s/xfug1x/$fug/g" mpmc.inp
            sed -i "s/xfug2x/$fug/g" mpmc.inp
            sed -i "s/xtempx/$temp/g" mpmc.inp

            cp ../../INPUT.pdb .
            cp ../../INSERT.pdb .

            rm -f core.*
            rm -f std*

            bsub < mpmc_submit.sh
            pwd
 
            cd ../
        done
        cd ../
    done
    cd ../
done
