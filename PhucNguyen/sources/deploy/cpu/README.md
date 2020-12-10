<!-- for CPU server -->

location=/opt/webapps/Phuc_FCI20200819
env_path=/opt/webapps/Phuc_FCI20200819/fcienv


<!-- 1/ Install packages, virtualenv  -->
sudo apt-get install -y graphviz
sudo apt-get install -y libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
sudo pip3 install -y virtualenv

<!-- Install Homebrew -->
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

<!-- Install Dlib -->
brew cask install xquartz
brew install gtk+3 boost
brew install boost-python --with-python3
pip install numpy scipy matplotlib scikit-image scikit-learn ipython
<!-- Install in system -->
brew install dlib 
<!-- Install in venv -->
pip install dlib


<!-- Create venv -->
virtualenv -p python3 ${env_path}

source ${env_path}/bin/activate
pip install -r ${location}/facecheckin/deploy/cpu/requirements.txt

<!-- Testing -->

cd ${location}/facecheckin/streaming/
python app.py --host <ip>
<!-- ex, $python app.py --host 172.16.7.43 -->
<!-- See http://172.16.7.43:8001/ -->