<!-- Autorun Start Up -->
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart 
@python3 /home/pi/Documents/thesis/app.py

<!-- Transform pyqt5 to .py -->
pyuic5 -x uiempty.ui -o ui.py

<!-- Run app -->
python3 run/app.py

<!-- Test app by flask -->
python3 test/apptest.py

<!-- unofficial userspace V4L2 driver for the Raspberry Pi Camera Module -->
uv4l --driver raspicam --auto-video_nr

<!-- Fast API -->
uvicorn main:app --reload

https://realpython.com/python-sockets/


<!-- Kafka -->
systemctl daemon-reload
sudo systemctl start zookeeper
sudo systemctl start kafka
sudo systemctl status kafka

34.87.138.205
34.87.104.34

<!-- Server Python -->
mkdir ailibs_data/data
