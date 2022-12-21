import logging
import os
import time

import grpc
from time import time
import file_pb2 as file_pb2
import file_pb2_grpc as file_pb2_grpc

logger = logging.getLogger(__name__)

UPLOAD_BLOCK_SIZE = 1024*1024*2 

class FileClient:
  def __init__(self, ip_address, port,trusted_cert=None):
    self.__ip_address = ip_address
    self.__port = port

    # credentials = grpc.ssl_channel_credentials(root_certificates=trusted_cert)
    # channel = grpc.secure_channel("{}:{}"
    #   .format(self.__ip_address, self.__port), credentials)
    
    channel = grpc.insecure_channel(f"{ip_address}:{port}")
    self.stub = file_pb2_grpc.FileStub(channel)
    self.channel=channel


  def uploadSetName(self,filename,full_file_name):
    return self.stub.uploadSetName(file_pb2.FileSetNameReq(name=filename,filesize=os.path.getsize(full_file_name)))

  def upload(self,full_file_name,progressCallback=None):
    return self.stub.upload(self._upload(full_file_name,progressCallback))

  def _upload(self,full_file_name,progressCallback):
    filesize = os.path.getsize(full_file_name)
    uplaodedSize = 0
    t = time()
    if os.path.isfile(full_file_name):
      with open(full_file_name, "rb") as fh:
        while True:
          piece = fh.read(UPLOAD_BLOCK_SIZE)
          if len(piece) == 0:
            break
          
          yield file_pb2.FileUploadReq(buffer=piece)
          uplaodedSize+=UPLOAD_BLOCK_SIZE
          print(f'speed:{uplaodedSize/1024/1024/(time()-t)}MB/s')
          if progressCallback:
            progressCallback(filesize,uplaodedSize)
            pass
    else:
      yield file_pb2.FileUploadReq()

  # def __str__(self):
  #   return "ip:{ip_address}, port:{port}, cert_file:{cert_file}"\
  #     .format(
  #       ip_address=self.__ip_address,
  #       port=self.__port,
  #       cert_file=self.__cert_file)
  def close(self):
    self.channel.close()
