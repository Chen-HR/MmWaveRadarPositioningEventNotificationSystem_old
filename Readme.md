# mmWave Radar System

## Library dependencies

### For Core Library

#### `pyserial`: 3.5

```cli
python -m pip install pyserial==3.5
```

#### `numpy`: 1.26.0

```cli
python -m pip install numpy==1.26.0
```

#### `PyMySQL`: 1.1.0

```cli
python -m pip install PyMySQL==1.1.0
```

#### `mysql-connector-python`: 8.2.0

```cli
python -m pip install mysql-connector-python==8.2.0
```

#### `line-bot-sdk`: 2.4.2

```cli
python -m pip install line-bot-sdk==2.4.2
```

#### [`github.com/Chen-HR/Ti_mmWave_Demo_Driver`](https://github.com/Chen-HR/Ti_mmWave_Demo_Driver): 1.0

```cli
git clone https://github.com/Chen-HR/Ti_mmWave_Demo_Driver.git
```

#### [`github.com/Chen-HR/HAClusteringTool`](https://github.com/Chen-HR/HAClusteringTool): 1.0

```cli
git clone https://github.com/Chen-HR/HAClusteringTool.git
```

#### `pyzenbo`: 1.0.46.2220

```cli
# # if use powershell
# Expand-Archive -Path "Packages\pyzenbo_v1.0.46.2220.zip" -DestinationPath "Packages\pyzenbo_v1.0.46.2220"
# # if use cmd
# expand "Packages\pyzenbo_v1.0.46.2220.zip" -f:* "Packages\pyzenbo_v1.0.46.2220"
# # if use bash
# unzip "Packages\pyzenbo_v1.0.46.2220.zip" -d "Packages\pyzenbo_v1.0.46.2220"

cd Packages/pyzenbo_v1.0.46.2220/pyzenbo
python setup.py install
cd ../../..
```
