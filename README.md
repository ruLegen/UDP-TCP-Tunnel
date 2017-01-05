# UDP-Tunnel

## Requerements
+ Python 2.7 or higher
+ Python packages
 * requests - Requests HTTP library
 * json
 * time
 
 ---
 
## Usage
 <pre>python client.py [--sourceport SOURCEPORT] [--remoteport REMOTEPORT]
                 [--sourcehost SOURCEHOST] [--remotehost REMOTEHOST]
                 [--username USERNAME] [--remoteusername REMOTEUSERNAME]
                 [--directconnection] [--signalserver SIGNALSERVER]
                 [--forcename FORCENAME] [-h]
</pre>
  <pre>
  -h, --help            show this help message and exit
  --directconnection, -d
                        Connect without Signal Server.
  --sourceport SOURCEPORT, -sp SOURCEPORT
                        Source port wich from will be enstabilish connect.
                        Default is 9876
  --remoteport REMOTEPORT, -rp REMOTEPORT
                        Remote port to enstabilish connect. Default is 9876
  --sourcehost SOURCEHOST, -sh SOURCEHOST
                        Host wich will trying connect. Default is 0.0.0.0
  --remotehost REMOTEHOST, -rh REMOTEHOST
                        Remote host
                        
 </pre>
---                        
<pre>
if flag -directconnection is not set will use next vars

  --username USERNAME, -u USERNAME
                        Your name for register in Signal server
  --remoteusername REMOTEUSERNAME, -ru REMOTEUSERNAME
                        Remote username to connect
  --signalserver SIGNALSERVER, -ss SIGNALSERVER
                        Signal server IP or Domain
                        http://some_domain.com[:some_port]
  --forcename FORCENAME, -f FORCENAME
                        Use the registered name. Use already existing name

  </pre>
