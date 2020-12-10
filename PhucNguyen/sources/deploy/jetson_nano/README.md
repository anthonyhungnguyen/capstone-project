<!-- for Jetson nano -->

location=/opt/webapps/Phuc_FCI20200819
env_path=/opt/webapps/Phuc_FCI20200819/fcienv
cv2_path=/home/jetson1/workspace/opencv/cv2.so


<!-- 1/ Install packages, virtualenv  -->
sudo apt-get install -y graphviz
sudo apt-get install -y libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
sudo pip3 install -y virtualenv


<!-- Create venv -->
virtualenv -p python3 ${env_path}

source ${env_path}/bin/activate
pip install -r ${location}/facecheckin/deploy/jetson_nano/requirements.txt
<!-- ~ 2 hours waiting -->

<!-- tensorflow -->
#pip install numpy<1.17
sudo apt-get update
sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
pip install -U numpy==1.16.1 future==0.18.2 mock==3.0.5 h5py==2.10.0 keras_preprocessing==1.1.1 keras_applications==1.0.8 gast==0.2.2 futures protobuf pybind11
pip install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v44 tensorflow==2.2.0+nv20.8

<!-- dlib -->

cd ${location}
wget http://dlib.net/files/dlib-19.21.tar.bz2
tar xvf dlib-19.21.tar.bz2
<!-- Update /dlib/cuda/cudnn_dlibapi.cpp -> com //forward_algo = forward_best_algo; line 854  -->
<!-- https://forums.developer.nvidia.com/t/issues-with-dlib-library/72600/16 -->
cd dlib-19.21/
mkdir build
cd build
cmake ..
cmake --build . --config Release
sudo make install
sudo ldconfig

source ${env_path}/bin/activate

cd dlib-19.21
python setup.py install

rm -rf dist
rm -rf tools/python/build
rm python_examples/dlib.so
<!-- or -->
pip install dlib


<!-- link cv2 -->
ln -s ${cv2_path} ${env_path}/lib/python3.6/site-packages/cv2.so

<!-- Testing -->

cd ${location}/facecheckin/streaming/
python app.py --host <ip>
<!-- ex, $python app.py --host 172.16.7.43 -->
<!-- See http://172.16.7.43:8001/ -->


<!-- for static IP -->
sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio