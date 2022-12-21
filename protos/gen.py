import os

application_path = os.path.dirname(__file__)+'\\'
application_path=application_path.replace('/','\\')
application_path_parent =  os.path.abspath(application_path+'..')+'\\'

os.chdir(application_path)
os.system(f'python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. file.proto')
os.system(f'copy file_pb2_grpc.py ..\\client\\')
os.system(f'copy file_pb2.py ..\\client\\')
os.system(f'copy file_pb2_grpc.py ..\\server\\')
os.system(f'copy file_pb2.py ..\\server\\')

