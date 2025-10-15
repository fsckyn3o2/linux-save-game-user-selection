#!/bin/bash
cdir=$(dirname ${BASH_SOURCE[0]})

logfile="${cdir}/execution.log"
date_exec=$(date +"%Y-%m-%d %H:%M:%S")
prefix_log="$date_exec :: "

FILE_TO_CHECK="$logfile" # Replace with the actual file name
SIZE_LIMIT_BYTES=1048576 # 1 MB (10 * 1024 * 1024 bytes)

if [ -f "$FILE_TO_CHECK" ]; then # Check if the file exists
    FILE_SIZE=$(stat -c %s "$FILE_TO_CHECK") # Get file size in bytes
    if (( FILE_SIZE > SIZE_LIMIT_BYTES )); then
        echo "File '$FILE_TO_CHECK' exceeds ${SIZE_LIMIT_BYTES} bytes. Removing..."
        echo "" > $logfile
    else
        echo "File '$FILE_TO_CHECK' is within the size limit."
    fi
else
  touch $logfile
fi

GAMEDIR=$(basename "$HEROIC_GAME_PREFIX")

# MAPPING OF HEROIC GAME TITLE TO A GAME KEY
echo "$prefix_log Execution of this script with environment variables" >> $logfile
echo "$prefix_log  HEROIC_GAME_APP_NAME=$HEROIC_GAME_APP_NAME" >> $logfile
echo "$prefix_log  HEROIC_GAME_EXEC=$HEROIC_GAME_EXEC" >> $logfile
echo "$prefix_log  HEROIC_GAME_PREFIX=$HEROIC_GAME_PREFIX" >> $logfile
echo "$prefix_log  HEROIC_GAME_RUNNER=$HEROIC_GAME_RUNNER" >> $logfile
echo "$prefix_log  HEROIC_GAME_SCRIPT_STAGE=$HEROIC_GAME_SCRIPT_STAGE" >> $logfile
echo "$prefix_log  HEROIC_GAME_TITLE='$HEROIC_GAME_TITLE'" >> $logfile
echo "$prefix_log  GAMEDIR='$GAMEDIR'" >> $logfile
echo "$prefix_log Execution of command 'python ${cDir}/main.py -g $HEROIC_GAME_APP_NAME -d $GAMEDIR'" >> $logfile
python ${cDir}main.py --game $HEROIC_GAME_APP_NAME --dir $GAMEDIR >> $logfile