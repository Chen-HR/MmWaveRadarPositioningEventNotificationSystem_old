
python -m pip install pyserial==3.5
python -m pip install numpy==1.26.0
python -m pip install mysql-connector-python==8.2.0
python -m pip install line-bot-sdk==2.4.2

git clone https://github.com/Chen-HR/Ti_mmWave_Demo_Driver.git
git clone https://github.com/Chen-HR/HAClusteringTool.git

Expand-Archive -Path "Packages\pyzenbo_v1.0.46.2220.zip" -DestinationPath "Packages\pyzenbo_v1.0.46.2220"
cd Packages/pyzenbo_v1.0.46.2220/pyzenbo
python setup.py install
cd ../../..
