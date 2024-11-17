steps=`grep "Completed step" runlog.log | awk '{print $4}' | sed 's:/[^/]*$::' | awk '!/matches/'`
mmolg=`grep "wt % (ME)" runlog.log | awk '{print ($6*10/2.01594)}'`
N=`grep "N =" runlog.log | awk {'print $4'}`
pe=`grep "potential energy" runlog.log | awk {'print $5'}`

steps="0\n1000\n$steps"

echo -e "$steps" | paste -d '\t' - <(echo "$mmolg") | paste -d '\t' - <(echo "$N") | paste -d '\t' - <(echo "$pe") > data.txt
