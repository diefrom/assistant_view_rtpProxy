#!/bin/sh

OPEN_FILE=$1
grep 'futex.*,' $OPEN_FILE > $OPEN_FILE.tmp
NEW_OPEN_FILE=$OPEN_FILE.tmp
LOG_FILE=count_$OPEN_FILE
lock=("")
value=(0)
i=0

if [ -f $LOG_FILE ]; then
    rm $LOG_FILE -rf 
fi

while read LINE; do
    flag="false"
    address_temp=${LINE#*(} 
    address=${address_temp%%,*}
    if [ "$address" == "$LINE" ]; then
        continue
    fi
    len=${#lock[*]}
    for ((j=0; j<len; j++));do
        if [ "${lock[j]}" == "$address" ]; then
            ((value[j]++))
            flag="true"
            break
        fi  
    done

    if [ "$flag" == "false" ]; then
        lock[i]=$address
        value[i]=1
        ((i++))
    fi
done < $NEW_OPEN_FILE

len=${#lock[*]}
for ((j=0; j<len; j++)); do
    #num=`grep -o "${lock[j]}" $OPEN_FILE| wc -l`
    echo "address:${lock[j]} num=${value[j]}" >> $LOG_FILE
done
rm $NEW_OPEN_FILE -f
