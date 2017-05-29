where python>tmp
set /p pythonpath=<tmp
set pythonpath=%pythonpath:\=\\%
set dir=%cd%
set dir=%cd:\=\\%
del tmp

echo REGEDIT4 > tunnel.reg

echo [HKEY_CLASSES_ROOT\tunnel] >> tunnel.reg

echo @="URL:tunnel" >> tunnel.reg

echo "URL Protocol"="" >> tunnel.reg

echo [HKEY_CLASSES_ROOT\tunnel\DefaultIcon] >> tunnel.reg

echo @="\"%pythonpath%\"" >> tunnel.reg

echo [HKEY_CLASSES_ROOT\tunnel\shell] >> tunnel.reg

echo [HKEY_CLASSES_ROOT\tunnel\shell\open] >> tunnel.reg

echo [HKEY_CLASSES_ROOT\tunnel\shell\open\command] >> tunnel.reg

echo @="\"%pythonpath%\" \"%dir%\\program_udp\\client.py\" \"%%1\"" >> tunnel.reg


echo REGEDIT4 > webhandler.reg

echo [HKEY_CLASSES_ROOT\webhandler] >> webhandler.reg

echo @="URL:webhandler" >> webhandler.reg

echo "URL Protocol"="" >> webhandler.reg

echo [HKEY_CLASSES_ROOT\webhandler\DefaultIcon] >> webhandler.reg

echo @="\"%pythonpath%\"" >> webhandler.reg

echo [HKEY_CLASSES_ROOT\webhandler\shell] >> webhandler.reg

echo [HKEY_CLASSES_ROOT\webhandler\shell\open] >> webhandler.reg

echo [HKEY_CLASSES_ROOT\webhandler\shell\open\command] >> webhandler.reg

echo @="\"%pythonpath%\" \"%dir%\\program_udp\\webhandler.py\" \"%%1\"" >> webhandler.reg


