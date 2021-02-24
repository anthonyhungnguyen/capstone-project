<!-- Autorun Start Up -->
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart 
@python3 /home/pi/Documents/thesis/app.py

<!-- Transform pyqt5 to .py -->
pyuic5 -x uiempty.ui -o ui.py

<!-- Run app -->
python3 run/app.py

<!-- Test app by flask -->
python3 test/apptest.py
