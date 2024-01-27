# %%
import time
import threading
# import os
# import math
import datetime
import dataclasses

import numpy # numpy-1.26.0
import matplotlib # matplotlib-3.8.1
# import mysql.connector # mysql-connector-python-8.2.0

from Ti_mmWave_Demo_Driver import Ti_mmWave
# from Ti_mmWave_Demo_Driver import Configuration
from Ti_mmWave_Demo_Driver import DataFrame
from Ti_mmWave_Demo_Driver import Logging
# from Ti_mmWave_Demo_Driver import SerialTool

import HAClusteringTool

import Notify

from Config import config

# %%
if config.language != "en-US" and config.language != "zh-TW": config.language = "en-US"

limit      = config.detection.limit
scale      = config.detection.scale
TimeToLive = config.detection.TimeToLive

x_range = config.scene.x_range
y_range = config.scene.y_range
z_range = config.scene.z_range

crc32: numpy.uint32 = 0
earlier = set()
predict = None
ttl = 0

if config.mode == "Error statistics":
  locationPoint = (0, 1.4, 0)
  records = list()

# %%
def get_detectedPoints(device: Ti_mmWave, CRC32: numpy.uint32) -> list[tuple]:
  # print(f"device.data.CRC32: {device.data.CRC32}")
  if device.data.CRC32 == crc32: return False
  return [(DataFrame.Converter.QFormat.parse(device.data.detectedObjects.infomation.xyzQFormat, DetectedObj.x), DataFrame.Converter.QFormat.parse(device.data.detectedObjects.infomation.xyzQFormat, DetectedObj.y), DataFrame.Converter.QFormat.parse(device.data.detectedObjects.infomation.xyzQFormat, DetectedObj.z)) for DetectedObj in device.data.detectedObjects.Objects]

def filter_points(points, x_range, y_range, z_range):
  filtered_points = []
  if points is not None:
    for point in points:
      x, y, z = point
      if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1] and z_range[0] <= z <= z_range[1]:
        filtered_points.append(point)
  return filtered_points
def nearestPoint(points: list[tuple], target_point = (0, 0, 0)):
  min_distance = float('inf')
  nearest = None
  for point in points:
    distance = HAClusteringTool.Calculator.distance(target_point, point)
    if distance < min_distance:
      min_distance, nearest = distance, point
  return nearest
def vectorOffset(target: tuple, source: tuple = (0, 0, 0)) -> tuple:
  return tuple(numpy.array(target) - numpy.array(source))
def vectorMove(offset: tuple, source: tuple = (0, 0, 0)) -> tuple:
  return tuple(numpy.array(offset) + numpy.array(source))
def vectorScale(source: tuple, scale) -> tuple:
  return tuple(numpy.array(source) * scale)
def vectorPredict(current: tuple, previous: tuple = (0, 0, 0), scale = 1.0) -> tuple:
  return (vectorMove(vectorScale(vectorOffset(current, previous), -scale), previous), vectorMove(vectorScale(vectorOffset(current, previous), scale), previous))
class Timer:
  def __init__(self):
    self.starttime = 0.0
  def start(self):
    self.starttime = time.time()
  def now(self):
    return time.time() - self.starttime
timer = Timer()

# %%
timer.start()
device = Ti_mmWave(config.device.platform, config.device.Ctrl_port_name, config.device.Data_port_name, Parse_timeInterval=0.2)
# device.logger.echo = True
# device.config.logger.echo = True
# device.data.logger.echo = True
# print("configured device...")
device.sensorStop(log=config.device.log)
device.Ctrl_Load_file(config.device.Config_File_name)
device.config.set_CfarRangeThreshold_dB(threshold_dB=config.device.CfarRangeThreshold_dB)
device.config.set_RemoveStaticClutter(enabled=config.device.RemoveStaticClutter)
# device.config.set_RemoveStaticClutter(enabled=False)
device.config.set_FramePeriodicity(FramePeriodicity_ms=config.device.FramePeriodicity) # get as `device.config.parameter.framePeriodicity`
device.Ctrl_Send()
device.sensorStart(log=config.device.log)
# print("sensorStart")
print(f"setup device used {timer.now()} secend")
# %%
timer.start()
if config.alerter.lineBot.enabled: lineBot = Notify.LineBot(config.alerter.lineBot.access_token)
print(f"setup lineBot used {timer.now()} secend")
# %%
timer.start()
zenbots: list[Notify.ZenBot] = []
if config.alerter.zenBot.enabled: 
  if config.debug: print(f"{Logging.formatted_time(datetime.timezone(datetime.timedelta(hours=8)), '%Y-%m-%d %H:%M:%S.%f')}: {[user.zenbot_host for user in config.users]}")
  mode = ""
  if config.language == "zh-TW":  
    if config.mode == "Home Security"   : mode = "居家安全"
    if config.mode == "Error statistics": mode = "誤差統計"
    if config.mode == "Area Detection"  : mode = "區域檢測"
  if config.language == "en-US":  
    if config.mode == "Home Security"   : mode = "Home Security"
    if config.mode == "Error statistics": mode = "Error statistics"
    if config.mode == "Area Detection"  : mode = "Area Detection"

  for zenbot_host in [user.zenbot_host for user in config.users]:
    zenbots.append(Notify.ZenBot(zenbot_host))
    # if zenbots[-1].zenBot == None or zenbots[-1].zenBot.get_connection_state() != (1, 1): 
    #   print(f"Connection failed for zenBot Notify.ZenBot('{zenbot_host}')")
    #   if zenbots[-1].zenBot != None and zenbots[-1].zenBot.get_connection_state() != (1, 1): print(zenbots[-1].zenBot.get_connection_state())
    #   exit(1)
    if config.language == "en-US": zenbots[-1].expression(sentence=f"The millimeter wave radar system starts and turns on {config.mode} mode.")
    if config.language == "zh-TW": zenbots[-1].expression(sentence=f"毫米波雷達系統啟動，開啟{mode}模式")
    if config.mode == "Error statistics" and config.language == "en-US": zenbots[-1].expression(sentence=f"Please clear the environment and move to point P{locationPoint}")
    if config.mode == "Error statistics" and config.language == "zh-TW": zenbots[-1].expression(sentence=f"請淨空環境，並移動至點{locationPoint}的位置")
print(f"setup zenbot used {timer.now()} secend")

# %%
try:
  device.Data_Buffering_thread_start()
  device.Data_Parse_thread_start()

  if config.mode == "Error statistics": 
    Error_statistics_Timer = Timer()
    Error_statistics_Timer.start()

  while True:
    start_time = time.time()
    clustering_points = None
    targets = None

    # get the detected Points
# %%
    if config.debug: timer.start()
    detectedPoints = get_detectedPoints(device, crc32)

    # if is new data
    if detectedPoints != False:
      crc32 = device.data.CRC32
      detectedPoints_with_clustering = [detectedPoints]
      try:
        detectedPoints_with_clustering.append(HAClusteringTool.Calculator.cluster_centers(HAClusteringTool.clustering_V1(detectedPoints, limit)))
        # detectedPoints_with_clustering.append(HAClusteringTool.Calculator.cluster_centers(HAClusteringTool.clustering_V2_1(detectedPoints, limit, 0.8)))
        # detectedPoints_with_clustering.append(HAClusteringTool.Calculator.cluster_centers(HAClusteringTool.clustering_V2_2(detectedPoints, limit, 0.8)))
        # detectedPoints_with_clustering.append(HAClusteringTool.Calculator.cluster_centers_of_gravity(HAClusteringTool.clustering_V2_2(detectedPoints, limit, 0.8, True)))
      except ValueError:
        pass
      except ZeroDivisionError:
        pass
      clustering_points = HAClusteringTool.Calculator.cluster_centers(HAClusteringTool.pairing(detectedPoints_with_clustering, limit, useVirtualPoints=True))
      clustering_points = filter_points(clustering_points, x_range, y_range, z_range)

      # TODO: filter detection points by scene
      targets = filter_points(clustering_points, x_range, y_range, z_range)
    if config.debug: 
      _t = timer.now()
      if _t != 0: print(f"get the detected Points {timer.now()} secend")


    # Error statistics
    if targets is not None and config.mode == "Error statistics":
      records.append(targets)

    if targets is not None and config.mode != "Error statistics":
      ttl = TimeToLive
      # print(f"{Logging.formatted_time(datetime.timezone(datetime.timedelta(hours=8)), '%Y-%m-%d %H:%M:%S.%f')}: ", end="")
      areas: set[str] = set()
      if len(targets) != 0:
        # if config.debug: print(f"{Logging.formatted_time(datetime.timezone(datetime.timedelta(hours=8)), '%Y-%m-%d %H:%M:%S.%f')}: {ttl}: targets: {targets}")
        for target in targets:
          for area in config.scene.areas:
            if area.x_range[0]<=target[0]<=area.x_range[1] and area.y_range[0]<=target[1]<=area.y_range[1] and area.z_range[0]<=target[2]<=area.z_range[1]:
              areas.add(area.name)
              break

      # Area Detection. 
      if config.mode == "Area Detection":
        if len(areas)>0 and config.mode == "Area Detection": 
          if config.language == "en-US": msg = "There are people in areas "
          if config.language == "zh-TW": msg = "There are people in areas "
          msg = ""
          for area in areas:
            msg += str(area) + ", "
          msg = msg[:-2]
          print(msg, end="")
          if msg != "":
            if config.alerter.lineBot.enabled: lineBot.multicast([user.lineId for user in config.users], msg)
            if config.alerter.zenBot.enabled: [zenbot.expression(sentence=msg) for zenbot in zenbots]
        # print()
      
      # Home Security
      if config.mode == "Home Security":
        if config.debug: print(f"{Logging.formatted_time(datetime.timezone(datetime.timedelta(hours=8)), '%Y-%m-%d %H:%M:%S.%f')}: {config.mode}: {earlier}, {areas}")
        if len(areas)>0 and config.mode == "Home Security": # "danger zone" ,  "Near dangerous areas",  "Door"        ,  "Entrance"    ,  "Outside"     ,
          msg = ""
          if len(earlier)>0:

            # SceneArea.type = 1
            if "danger zone" in areas and "danger zone" not in earlier:
              if config.language == "en-US": msg += "Someone has entered the danger zone. "
              if config.language == "zh-TW": msg += "有人進入了危險區域。"
            if "Near dangerous areas" in areas and "Near dangerous areas" not in earlier:
              if config.language == "en-US": msg += "Someone is near the danger zone. "
              if config.language == "zh-TW": msg += "有人在危險區域附近。"

            # SceneArea.type = 2
            if "Door" in areas and "Entrance" in earlier or "Outside" in areas and "Entrance" in earlier:
              if config.language == "en-US": msg += "Please be careful when going out. "
              if config.language == "zh-TW": msg += "出門請小心。"
            if "Entrance" in areas and "Outside" in earlier or "Door" in areas and "Outside" in earlier:
              if config.language == "en-US": msg += "Welcome back. "
              if config.language == "zh-TW": msg += "歡迎回來。"

          earlier = {area for area in areas}
          if msg != "":
            if config.alerter.lineBot.enabled: lineBot.multicast([user.lineId for user in config.users], msg=msg)
            if config.alerter.zenBot.enabled: 
              # def zenbots_alarter(zenbots: list[ZenBot], msg: str, time=Logging.formatted_time(datetime.timezone(datetime.timedelta(hours=8)), '%Y-%m-%d %H:%M:%S.%f')):
              #   if config.debug: timer.start()
              #   _return = [zenbot.expression(sentence=msg) for zenbot in zenbots]
              #   if config.debug: print(f"{time}: zenBot alert used {timer.now()} secend")
              #   return _return
              # threading.Thread(target=zenbots_alarter, args=(zenbots, msg), )
              if config.debug: timer.start()
              [zenbot.expression(sentence=msg) for zenbot in zenbots] 
              if config.debug: print(f"{time}: zenBot alert used {timer.now()} secend")
          print(f"{Logging.formatted_time(datetime.timezone(datetime.timedelta(hours=8)), '%Y-%m-%d %H:%M:%S.%f')}: {msg}")

    elif targets is None:
      ttl = ttl-1 if ttl > 0 else 0
      if ttl == 0: earlier = set()

    while (time.time()-start_time) < (device.config.parameter.framePeriodicity/1000)/4:
      pass

    if config.mode == "Error statistics" and Error_statistics_Timer.now() > 60: break

    # print(Logging.formatted_time(datetime.timezone(datetime.timedelta(hours=8)), "%Y-%m-%d %H:%M:%S.%f"))
except RuntimeError as error:
  print(f"{Logging.formatted_time(datetime.timezone(datetime.timedelta(hours=8)), '%Y-%m-%d %H:%M:%S.%f')}: {error}")
except KeyboardInterrupt: 
  device.Data_Buffering_thread_stop()
  device.Data_Parse_thread_stop()

if config.mode == "Error statistics":
  print(records)
# %%
if config.alerter.zenBot.enabled and config.language == "en-US":  [zenbot.expression(sentence="Millimeter wave radar system shutdown") for zenbot in zenbots]
if config.alerter.zenBot.enabled and config.language == "zh-TW":  [zenbot.expression(sentence="毫米波雷達系統關閉") for zenbot in zenbots]
del device
# %%
