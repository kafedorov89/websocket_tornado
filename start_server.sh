service mysql stop
ssh -L 3306:127.0.0.1:3306 -f -N root@149.154.66.148 sleep 10
cd /home/kos/Git/websocket_tornado/
python server.py 
