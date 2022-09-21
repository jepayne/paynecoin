#!/bin/bash
if [ -z "$1" ] || ( [ $1 != "init" ] && [ $1 != "list" ] && [ $1 != "kill" ] )
then
    echo "argument must be one of: 'init [port]', 'list', or 'kill'"
else
    if [ $1 = "init" ]
    then
        if [ -z "$2" ]
        then
            END=0
        else
            END=$(($2-1))
        fi
        BASE_PORT=5001
        declare -a namearr=("alice" "bob" "carol" "dave" "eve" "frank" "george" "harry" "iris" "james")
        for i in $(seq 0 $END)
            do
                if [ $i -lt 10 ] # for the first 10 ports, associate a name from above
                then
                    PORT=$(($BASE_PORT+$i))
                    nohup python api.py -p $PORT -u ${namearr[$i]} > /dev/null 2>&1 &
                else
                    PORT=$(($BASE_PORT+$i))
                    nohup python api.py -p $PORT > /dev/null 2>&1 &
                fi
            done
    elif [ $1 = "list" ]
    then
        ps ax | grep api.py | grep -v grep
    elif [ $1 = "kill" ]
    then
        ps ax | grep api.py | grep -v grep | awk '{print $1}' | xargs kill
    fi
fi
