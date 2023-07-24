#!/bin/bash

base=$(pwd)

for temp in 220 230 240 250; do
        cd $temp

        echo ""
        echo $temp
        echo "kPa cm3/g"
        echo "0.0 0.0"

        for pressure in 0.0003 0.0005 0.0008 0.001 0.002; do
                cd $pressure

                kpa=`echo "$pressure * 101.3" | bc -l`
                cm3=`grep "wt % (ME) =" runlog.log | awk 'END{print ($6*10)/(131.293)*22.4}'`

                echo $kpa $cm3

                cd ../
        done
        cd ../
done
