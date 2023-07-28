#!/bin/bash

base=$(pwd)

rm *dat

for gas in h2 n2 ne; do
	cd $gas
	for orca in orca; do
		cd $orca
		if [[ "$gas" == "h2" ]]; then
			for config in `seq 1 200`; do
				cd $config
				grep FINAL runlog.log | awk 'BEGIN {a=0} {a+=NR==1?$5:-$5} END {print a*315775.02480407}'  >> $base/h2.dat
				cd ../
			done
		fi

		if [[ "$gas" == "h2" ]]; then
			for config in `seq 1 200`; do
				cd $config
				grep FINAL runlog.log | awk 'BEGIN {a=0} {a+=NR==1?$5:-$5} END {print a*315775.02480407}' >> $base/n2.dat
				cd ../
			done
		fi

		if [[ "$gas" == "ne" ]]; then
			for config in `seq 1 20`; do
				cd $config
				grep FINAL runlog.log | awk 'BEGIN {a=0} {a+=NR==1?$5:-$5} END {print a*315775.02480407}' >> $base/ne.dat
				cd ../
			done
		fi
		cd ../
	done
	cd ../
done
