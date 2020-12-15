# deploy/jetson_nano
<!-- clone source  -->

<!-- 1. Creating storage -->
cd FCI/
<!-- mkdir storage
mkdir storage/images
<!-- save crop face image by user_id -->
<!-- mkdir storage/dbfaces            -->
<!-- save face features -->
<!-- mkdir storage/dbfeatures -->
<!-- save face classifers -->
<!-- mkdir storage/dbclassifiers --> -->


<!-- 2. Creating fcienv -> deploy/jetson_nano -->

<!-- 3. Creating video streaming -->
<!-- update ../streaming/camera_opencv -->
<!-- line 68, video name -->
<!-- line 98, MODE_FACE_REGISTERING -->
<!-- ailibs_data at  P:\nartin\AIInternship2020\FCI-->


<!-- for facecheckin API -->
source ../fcienv/bin/activate
pip install Django==2.2.2
pip install django-cors-headers==3.0.2

cd ../FCI/sources/
<!-- update IP in ../checkin/settings.py -->
python manage.py makemigrations
python manage.py makemigrations facecheckin
python manage.py migrate --run-syncdb
<!-- update came ra configs -->
python tests/config_camera.py
<!-- python tests/create_record_images.py -->

<!-- fuser -n tcp -k 8000 -->
python manage.py runserver 172.16.30.13:8000
