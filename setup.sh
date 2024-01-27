
pip3 install pyserial==3.5 numpy==1.26.0 mysql-connector-python==8.2.0 line-bot-sdk==2.4.2

git clone https://github.com/Chen-HR/Ti_mmWave_Demo_Driver.git
git clone https://github.com/Chen-HR/HAClusteringTool.git

unzip "Packages\pyzenbo_v1.0.46.2220.zip" -d "Packages\pyzenbo_v1.0.46.2220"
cd Packages/pyzenbo_v1.0.46.2220/pyzenbo
python setup.py install
cd ../../..
