#!/bin/bash

BIN_PATH=~/.bin
DESKTOP_CONFIG_PATH=/usr/share/applications
echo "Creating .bin in home directory"

STATUS=`mkdir $BIN_PATH`
echo $STATUS

STATUS=`ln -sf $PWD/program_udp/client.py $BIN_PATH/client.py`
echo $STATUS
STATUS=`ln -sf $PWD/program_udp/webhandler.py $BIN_PATH/webhandler.py`
echo $STATUS
echo "Creating protocol handler"
PYTHON_PATH=`which python`
FILE=$DESKTOP_CONFIG_PATH/tunnel.desktop
echo ""> $DESKTOP_CONFIG_PATH/tunnel.desktop
echo "[Desktop Entry]" >> $FILE
echo "Name=tunnel" >> $FILE
echo "Exec="$PYTHON_PATH $BIN_PATH/client.py "%u" >>$FILE
echo "Type=Application" >> $FILE
echo "Terminal=true">> $FILE
echo "MimeType=x-scheme-handler/tunnel;" >>$FILE
echo "x-scheme-handler/tunnel=tunnel.desktop" >> $DESKTOP_CONFIG_PATH/mimeapps.list
update-desktop-database $DESKTOP_CONFIG_PATH

FILE=$DESKTOP_CONFIG_PATH/webhandler.desktop
echo ""> $DESKTOP_CONFIG_PATH/webhandler.desktop
echo "[Desktop Entry]" >> $FILE
echo "Name=webhandler" >> $FILE
echo "Exec="$PYTHON_PATH $BIN_PATH/webhandler.py "%u" >>$FILE
echo "Type=Application" >> $FILE
echo "Terminal=true">> $FILE
echo "MimeType=x-scheme-handler/webhandler;" >>$FILE
echo "x-scheme-handler/webhandler=webhandler.desktop" >> $DESKTOP_CONFIG_PATH/mimeapps.list
update-desktop-database $DESKTOP_CONFIG_PATH
