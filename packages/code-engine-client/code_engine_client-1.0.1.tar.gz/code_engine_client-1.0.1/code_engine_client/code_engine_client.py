#!/usr/bin/python
# -*- coding: UTF-8 -*-

from urllib.request import urlopen 
import json
import websocket
import _thread
import grpc
import sys
from code_engine_client import bot_api_conn_grpc_pb2
from code_engine_client import bot_api_conn_grpc_pb2_grpc
import sys
import importlib
from concurrent.futures import ThreadPoolExecutor



class CodeEngineClient:
  bot_config_url = "https://apps-1254429489.cos.ap-beijing.myqcloud.com/enable_bot/enable_bot_config.json"
  event_ws_url = "ws://jimugaoshou.com:50510/code"
  cmd_svr_url = "jimugaoshou.com:50501"

  def __init__(self, openid, id):
    self.openid = openid
    self.id = id
    self.bot_config_map = {}
    self.drive_config_map = {}
    self.cmd_client = None
    self.event_client = None
    self.threads = None

  # outter functions
  def init(self):
    self.load_bot_config()
    self.load_drive_config()

  def run(self):
    self.init_net()
    self.init_threads()
    self.event_client.run_forever()

  def cmd_motor(self, bot_index, tag, x):
    print("cmd_motor")
    msg = self.format_cmd_motor_msg(bot_index, tag, x)
    self.send_cmd_msg(msg)

  def cmd_led(self, bot_index, tag, x):
    print("cmd_led")
    msg = self.format_cmd_led_msg(bot_index, tag, x)
    self.send_cmd_msg(msg)

  # end outter functions


  # inner functions
  def init_net(self):
    self.cmd_client = self.init_cmd_client()
    self.event_client =  self.init_event_client()

  # share cmd client, and not init event client, just for code engine svr
  def attach_net(self, cmd_client):
    self.cmd_client = cmd_client

  # thread pool
  def init_threads(self):
    self.threads = ThreadPoolExecutor(max_workers=10)

  def load_bot_config(self):
    self.bot_config_map = self.get_json_from_url(CodeEngineClient.bot_config_url)

  def load_drive_config(self):
    url = "https://imgs-1254429489.cos.ap-beijing.myqcloud.com/drive/"+self.openid+"/"+self.id+".json"
    self.drive_config_map = self.get_json_from_url(url)

  def get_json_from_url(self, url):
    html = urlopen(url)
    data = html.read()
    return json.loads(data)

  def init_cmd_client(self):
    print("init_cmd_client")
    channel = grpc.insecure_channel(CodeEngineClient.cmd_svr_url)
    return bot_api_conn_grpc_pb2_grpc.BotApiConnGrpcStub(channel)

  def init_event_client(self):
    websocket.enableTrace(True)
    return websocket.WebSocketApp(CodeEngineClient.event_ws_url,
                            on_open=self.event_on_open,
                            on_message=self.event_on_message,
                            on_error=self.event_on_error,
                            on_close=self.event_on_close)

  def event_on_open(self, ws):
    print("event_on_open")
    self.send_event_init_msg(ws)

  def event_on_message(self, ws, message):
    print("event_on_message")
    msg = json.loads(message)

    if msg["cmd"] == "event":
      self.event_loop(msg)

  def event_on_error(self, ws, error):
    print("event_on_error")

  def event_on_close(self, ws, close_status_code, close_msg):
    print("event_on_close")

  def event_loop(self, msg):
    print("event_loop")

    if msg["cmd"] == "event":
      self.process_event(msg)
    elif msg["cmd"] == "sensor":
      self.process_sensor(msg)

  def process_event(self, msg):
    module_name = self.get_local_module_name()
    function_name, param_cnt = self.get_seq_function_name(msg["seq"])

    if function_name != "":
      fun_path = module_name+"."+function_name
      self.threads.submit(self.dynamic_run, fun_path, param_cnt, msg["x"], msg["y"],'','','','')
    else:
      print("unknown msg")


  def process_sensor(self, msg):
    module_name = self.get_local_module_name()
    function_name, param_cnt = self.get_sensor_function_name(msg["model"])

    if function_name != "":
      fun_path = module_name+"."+function_name

      if msg["model"] == "line":
        self.threads.submit(self.dynamic_run, fun_path, param_cnt, msg["result"]["exist"], msg["result"]["offset"],'','','','')
      elif msg["model"] == "color":
        self.threads.submit(self.dynamic_run, fun_path, param_cnt, msg["result"]["r"], msg["result"]["g"],msg["result"]["b"],'','','')
      elif msg["model"] == "qrcode":
        self.threads.submit(self.dynamic_run, fun_path, param_cnt, msg["result"]["url"], '','','','','')
      elif msg["model"] == "tflite":
        self.threads.submit(self.dynamic_run, fun_path, param_cnt, msg["result"]["label"], msg["result"]["confidence"],msg["result"]["x"],msg["result"]["y"],msg["result"]["w"],msg["result"]["h"])

    else:
      print("unknown msg")


  def get_local_module_name(self):
    filename = sys.argv[0].split('/')[-1][0:-3]
    return filename

  def get_seq_function_name(self, seq):

    param_cnt = 1
    function_name = ""
    for unit in self.drive_config_map["units"]:
      if unit['seq'] == seq:
        if unit['ui']['type'] == "joystick":
          param_cnt = 2

        function_name = "on_event_"+unit['ui']['type']+"_"+str(seq)

    return function_name, param_cnt

  def get_sensor_function_name(self, model):
    param_cnt = 1
    function_name = ""

    if model == "line":
      param_cnt = 2
      function_name = "on_sensor_line"
    elif model == "color":
      param_cnt = 3
      function_name = "on_sensor_color"
    elif model == "tflite":
      param_cnt = 6
      function_name = "on_sensor_tflite"
    elif model == "qrcode":
      param_cnt = 1
      function_name = "on_sensor_qrcode"

    return function_name, param_cnt


  def reload_module(self, module_path):

    tmp = importlib.util.find_spec(module_path)
    if tmp == None:
        return None

    tmp = importlib.import_module(module_path)
    importlib.reload(tmp)

    return tmp

  def dynamic_run(self, fun_path, param_cnt, x1, x2, x3, x4, x5, x6):

    # try:
        module_path = fun_path.split('.')[0]
        fun_name = fun_path.split('.')[1]

        mod = self.reload_module(module_path)

        if hasattr(mod, fun_name):
          if param_cnt == 1:
            eval("mod."+fun_name)(self, x1)
          elif param_cnt == 2:
            eval("mod."+fun_name)(self, x1, x2)
          elif param_cnt == 3:
            eval("mod."+fun_name)(self, x1, x2, x3)
          elif param_cnt == 4:
            eval("mod."+fun_name)(self, x1, x2, x3, x4)
          elif param_cnt == 5:
            eval("mod."+fun_name)(self, x1, x2, x3, x4, x5)
          elif param_cnt == 6:
            eval("mod."+fun_name)(self, x1, x2, x3, x4, x5, x6)
        else:
            print("Error, no such function : "+fun_path)

    # except:
        # print("Error dynamic_run, fun_path : "+fun_path+", params : "+str(x1))


  def send_event_init_msg(self, ws):
    msg = {"openid": self.openid, "id": self.id, "cmd":"init"}
    data = json.dumps(msg)
    ws.send(data)


  def format_cmd_motor_msg(self, bot_index, tag, x):

    a1, a2 = self.get_pins_of_tag(tag)

    # format cmd
    msg = {
        "app_version":"1.0.0",
        "app_os": "api",
        "openid": self.openid,
        "cmd": "base",
        "bot_id": self.get_bot_id_of_index(bot_index),
        "a1": a1,
        "a2": a2,
        "speed": x
    }

    return msg

  def format_cmd_led_msg(self, bot_index, tag, x):
    # format cmd
    a1, a2 = self.get_pins_of_tag(tag)

    # format cmd
    msg = {
        "app_version":"1.0.0",
        "app_os": "api",
        "openid": self.openid,
        "cmd": "base",
        "bot_id": self.get_bot_id_of_index(bot_index),
        "a1": a1,
        "a2": a2,
        "speed": x
    }

    return msg

  def get_pins_of_tag(self, tag):
    return self.bot_config_map['control_bot']['base'][tag+'1'], self.bot_config_map['control_bot']['base'][tag+'2']

  def get_bot_id_of_index(self, bot_index):
    bots = self.drive_config_map["bots"]
    if bot_index < len(bots):
      return bots[bot_index]
    else:
      return ""

  def send_cmd_msg(self, msg):
    # format req
    req = bot_api_conn_grpc_pb2.SendBotMsgRequest(openid = msg["openid"], bot_id = msg["bot_id"], cmd = msg["cmd"], msg = json.dumps(msg))

    # send msg
    resp = self.cmd_client.SendBotMsg(req)


  # end inner functions
