from concurrent import futures
import logging
import os
import time

import grpc
import subprocess
import file_pb2 as file_pb2
import file_pb2_grpc as file_pb2_grpc

logger = logging.getLogger(__name__)

DETACHED_PROCESS=8

class FileServicer(file_pb2_grpc.FileServicer):
  _PIECE_SIZE_IN_BYTES = 1024 * 1024 # 1MB

  def __init__(self, files_directory,speedtest:bool = False):
    self.__files_directory = files_directory
    self.__uploadName = 'unname'
    self.__filesize = 0
    self.speedtest = speedtest

  def upload(self, request_iterator, context):

      if self.speedtest:
        for response in request_iterator:
            # print(f'收到{len(response.buffer)}')
            response
        return file_pb2.FileUploadRsp(result=f'测试结束')

      os.chdir(self.__files_directory)
      s = '服务器执行命令结果:'
      tempfilename = 'tempfile.tmp'
      tempfilepath = self.__files_directory + tempfilename
      try:
        with open(tempfilepath, "wb") as fh:
            for response in request_iterator:
              fh.write(response.buffer)
        if os.path.getsize(tempfilepath)==self.__filesize:
          print('upload completed')
        else:
          print('upload failed')
          return file_pb2.FileUploadRsp(result=s+'文件没有传完')
        
      except Exception as e:
        print('upload failed:',e)
        return file_pb2.FileUploadRsp(result=f'上传失败:{e}')

      
      # while self.__uploadName in os.popen(f'tasklist').read():
      #   os.system(f'taskkill /IM "{self.__uploadName}" /F')
      #   s+='结束服务器该游戏进程\n'

      
      if os.path.isfile(self.__uploadName):
        print(f'删除旧文件 {self.__uploadName}')
        os.remove(self.__uploadName)
      os.rename('tempfile.tmp', self.__uploadName)
        
      # subprocess.Popen([self.__uploadName],cwd=self.__files_directory,creationflags=DETACHED_PROCESS, close_fds=True,shell=True)
      # time.sleep(1)
      # if self.__uploadName in os.popen(f'tasklist').read():
      #   s+='开启服务成功'
      # else:s+='开启服务失败'
      s+='完成'
      return file_pb2.FileUploadRsp(result=s)

  def uploadSetName(self, request, context):
      self.__uploadName = request.name
      self.__filesize = request.filesize
      print(f'uploadSetName name:{request.name} filesize:{request.filesize}' )
      return file_pb2.FileSetNameRsp()

class FileServer():
  _ONE_DAY_IN_SECONDS = 60 * 60 * 24

  def __init__(self, ip_address, port:int, max_workers, files_directory,
   private_key=None, certificate_chain=None,speedtest:bool = False):
    self.ip_address=ip_address
    self.port=port
    self.__max_workers = max_workers
    self.__files_directory = files_directory

    self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=self.__max_workers))
    file_pb2_grpc.add_FileServicer_to_server(FileServicer(self.__files_directory, speedtest=speedtest), self.__server)
    # server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain,),))
    # self.__server.add_secure_port(self.__ip_address + ":" + self.__port, server_credentials)
    self.__server.add_insecure_port(f'{ip_address}:{port}')
    # logger.info("created instance " + str(self))

  def __str__(self):
    return f"ip:{self.ip_address},\
      port:{self.port},\
      max_workers:{self.__max_workers},\
      files_directory:{self.__files_directory}"

  def start(self):
    logger.info("starting instance " + str(self))
    self.__server.start()
    try:
      while True:
        time.sleep(FileServer._ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
      self.__server.stop(0)


