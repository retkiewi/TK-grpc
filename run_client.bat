
cd ImageFinderRabbitMqSetupApp
Rem docker-compose up -d
Rem call sbt run
cd ../Client
Rem python -m pip install -r requirements.txt
Rem start cmd /k python ColorFilterConsumer.py
Rem start cmd /k python DogFilterConsumer.py
Rem start cmd /k python SimilarityConsumer.py
start cmd /k python SizeFilterConsumer.py grpc
start cmd /k python SizeFilterConsumer.py
Rem start cmd /k python FacesFilterConsumer.py
start cmd /k python -m animal
start cmd /k python -m body
start cmd /k python -m style
start cmd /k python -m format
start cmd /k python App.py