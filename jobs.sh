function jobs {
    # grabs my jobs searching for string $1
    if [[ "$1" == "here" ]]; then
        if [[ "$2" == "count" ]]; then
        squeue -u $USER -o '%8i %3t %4p %18j %9M %12l %12L %17B %4C %5D %Z' -S -t,i | grep $(pwd) | grep -c ""
        elif [[ "$2" == "cancel" ]]; then
            for x in $(squeue -u $USER -o '%8i %3t %4p %18j %9M %12l %12L %17B %4C %5D %Z' -S -t,i | grep $(pwd) | awk {'print $1'}); do echo "canceling job $x"; scancel $x; done
        else
        squeue -u $USER -o '%8i %3t %4p %18j %9M %12l %12L %17B %4C %5D %Z' -S -t,i | grep $(pwd)
        fi
    elif [[ "$1" == "time" ]]; then
        squeue -u $USER -o '%8i %3t %4p %18j %9M %12l %12L %17B %4C %5D %Z' -S -t,i | tail -n +2 | awk {'printf("%18s  %9s\n",$4,$5)'} >> jobs.tmp
            str=""
            count=0
            while read p; do
                str=$str" | "$p;
                let count=$count+1
                if [[ "$count" -eq 5 ]]; then
                    echo $str" | "
                    str=""
                    count=0
                fi
            done < jobs.tmp
        rm jobs.tmp
        if [[ "$count" -ne 0 ]]; then
            echo $str" | "
        fi
    elif [[ "$1" == "running" ]]; then
        squeue -u $USER -o '%8i %3t %4p %18j %9M %12l %12L %17B %4C %5D %Z' -S -t,i | grep " R "
    else
        if [[ "$1" == "count" ]]; then
        squeue -u $USER -o '%8i %3t %4p %18j %9M %12l %12L %17B %4C %5D %Z' -S -t,i | grep -c ""
        elif [[ "$2" == "count" ]]; then
        squeue -u $USER -o '%8i %3t %4p %18j %9M %12l %12L %17B %4C %5D %Z' -S -t,i | grep -E 'JOBID|'$1'' | grep -c ""
        else
        squeue -u $USER -o '%8i %3t %4p %18j %9M %12l %12L %17B %4C %5D %Z' -S -t,i | grep -E 'JOBID|'$1''
        fi
    fi
}
