
import dataclasses
import typing

@dataclasses.dataclass
class EmailBot:
  enabled: bool = False
  host: str = ""
  port: int = 587
  name: str = ""
  user: str = ""
  password: str = ""

@dataclasses.dataclass
class LineBot:
  enabled: bool = False
  name: str = ""
  access_token: str = ""

@dataclasses.dataclass
class ZenBot:
  enabled: bool = False
  start: str = "Millimeter wave radar system started"
  stop: str = "Millimeter wave radar system shutdown"

@dataclasses.dataclass
class User:
  name: str
  email: typing.Optional[str] = None
  lineId: typing.Optional[str] = None
  zenbot_host: typing.Optional[str] = None

@dataclasses.dataclass
class MMWaveDevice:
  platform: str = ""
  Ctrl_port_name: str = ""
  Data_port_name: str = ""
  log: bool = False
  Config_File_name: str = ""
  CfarRangeThreshold_dB: float = 9.0
  RemoveStaticClutter: bool = False
  FramePeriodicity: int = 1000

@dataclasses.dataclass
class SceneArea:
  id: int = 0
  name: str = ""
  type: int = 0
  x_range: typing.Tuple[float, float] = (0.0, 0.0)
  y_range: typing.Tuple[float, float] = (0.0, 0.0)
  z_range: typing.Tuple[float, float] = (0.0, 0.0)

@dataclasses.dataclass
class Scene:
  id: int = 0
  name: str = ""
  x_range: typing.Tuple[float, float] = (0.0, 0.0)
  y_range: typing.Tuple[float, float] = (0.0, 0.0)
  z_range: typing.Tuple[float, float] = (0.0, 0.0)
  areas: typing.List[SceneArea] = dataclasses.field(default_factory=typing.List)

@dataclasses.dataclass
class Alerter:
  emailBot: EmailBot = dataclasses.field(default_factory=EmailBot)
  lineBot: LineBot = dataclasses.field(default_factory=LineBot)
  zenBot: ZenBot = dataclasses.field(default_factory=ZenBot)

@dataclasses.dataclass
class Detection:
  limit: float = 0.75
  TimeToLive: int = 20
  scale: float = 1.0

@dataclasses.dataclass
class Configuration:
  mode: str = ""
  debug: bool = False
  language: str = ""
  device: MMWaveDevice = dataclasses.field(default_factory=MMWaveDevice)
  users: typing.List[User] = dataclasses.field(default_factory=list)
  alerter: Alerter = dataclasses.field(default_factory=Alerter)
  detection: Detection = dataclasses.field(default_factory=Detection)
  scene: Scene = dataclasses.field(default_factory=Scene)

# config: Configuration = Configuration()