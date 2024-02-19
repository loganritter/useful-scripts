#!/bin/bash

base=$(pwd)

for gas in h2 n2; do
	cd $gas
	for temp in 77; do
		cd $temp
	
		echo ""
		echo $gas $temp
		echo "atm wtp mmol/g mmol/mmol kJ/mol N"
	
	        for pressure in 0.001 0.005 0.01 0.03 0.05 0.07 0.09 `seq 0.1 0.1 1.0`; do
			cd $pressure
			
			if [[ $gas == "h2" ]]; then	
				wtp=`grep "wt % (ME) =" runlog.log | tail -1 | awk {'print $6'}`
				mmolg=`grep "wt % (ME) =" runlog.log | awk 'END{print ($6*10/2.01594)}'`
				mmolmmol=`grep "wt % (ME) =" runlog.log | awk 'END{print ($6*10/2.01594/4.290756)}'`
			fi

			if [[ $gas == "n2" ]]; then
				wtp=`grep "wt % (ME) =" runlog.log | tail -1 | awk {'print $6'}`
                mmolg=`grep "wt % (ME) =" runlog.log | awk 'END{print ($6*10/28.0134)}'`
				mmolmmol=`grep "wt % (ME) =" runlog.log | awk 'END{print ($6*10/28.0134/4.290756)}'`

			fi
	
			qst=`grep "qst =" runlog.log | tail -1 | awk {'print $4'}`
			N=`grep "N =" runlog.log | tail -1 | awk {'print $4'}`

			echo $pressure $wtp $mmolg $mmolmmol $qst $N
		
			cd ../
		done
		cd ../
	done
	cd ../
done
