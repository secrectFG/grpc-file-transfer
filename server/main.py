import argparse
import logging
import os
import sys
import json
from myhelpers import readFileAllText
from server import FileServer

application_path = os.path.dirname(__file__)+'/'
application_path_parent =  os.path.abspath(application_path+'..')+'/'


# private_key = readAllBytes(application_path_parent+'cert/server.key')
# certificate_chain = readAllBytes(application_path_parent+'cert/server.crt')

def main():
  log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  logging.basicConfig(level=logging.INFO, format=log_fmt)
  logger = logging.getLogger(__name__)

  parser = argparse.ArgumentParser(description="gRPC file transfer server")
  parser.add_argument(
    "-s", "--speedtest", required=False, type=bool, help="Net Speed Test", default=True)
  # parser.add_argument(
  #   "-i", "--ip_adress", required=True, type=str, help="IP address for server")
  parser.add_argument(
    "-p", "--port", required=False, type=int, help="port address for server", default=16020)
  # parser.add_argument(
  #   "-w", "--max_workers",required=True, type=int, help="maximum worker threads for server")
  # parser.add_argument(
  #   "-d", "--files_directory", required=True, type=str, help="directory containing files")
  # parser.add_argument(
  #   "-priv", "--private_key_file", required=True, type=str, help="private key file path")
  # parser.add_argument(
  #   "-cert", "--cert_file", required=True, type=str, help="certificate file path")
  args = parser.parse_args()

  # logger.info(
  #   f"ip_adress:{args.ip_adress}, \
  #   port:{args.port}, \
  #   files_directory:{args.files_directory},")

  logger.info(f'args:{args}')



  server = FileServer(
    ip_address='[::]',
    port=args.port,
    max_workers=10,
    files_directory=application_path_parent,
    speedtest = args.speedtest,
    # private_key=private_key,
    # certificate_chain=certificate_chain
    )
  server.start()

if __name__ == "__main__":
  main()
