#!/bin/bash

for temp in 292; do
	cd $temp

	for pressure in `seq 0.1 0.1 1.0`; do
		cd $pressure

		tleft=`grep ETA runlog.log | tail -1`
		echo $tleft

		cd ../
	done
	cd ../
done
