# Prints job ID and directory
bjobsdir()
{
    job_id=`qstat -a | grep $USER | awk {'print $3'}`

    for i in $job_id; do 
        job_dir=`echo $i | xargs bjobs -l | grep -A 1 "CWD" | head -n 2 | paste -d " " - - | grep -o "CWD <[/a-zA-Z0-9.-\_]* *[/a-zA-Z0-9.-\_]*>" | sed "s/ //g" | sed "s/CWD//g" | sed "s/^<//g" | sed "s/>$//g"`
        echo $i $job_dir
    done
}

# Kill jobs located in current directory
bkill_here()
{
    base=`pwd`
    job_id=`bjobsdir | grep $base | awk {'print $1'}`

    for i in $job_id; do
        bkill $i
    done
}
