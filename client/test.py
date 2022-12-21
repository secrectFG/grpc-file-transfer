
import _winapi
import os
import subprocess
import time

def open_exe(fullpath,dir,args=[]):
    subprocess.Popen([fullpath]+args,cwd=dir,creationflags=subprocess.DETACHED_PROCESS|subprocess.CREATE_NEW_PROCESS_GROUP, close_fds=True,shell=True)



tasksStr = os.popen(f'tasklist').read()
if 'Router' in tasksStr:
    print('已打开')
else:
    # print(os.path.split(__file__))
    application_path=r'H:\SubGameServers\server_v2_netframework\Router\bin\Release\net5.0'
    open_exe(application_path+'/Router.exe',application_path,['18000'])
    time.sleep(2)
    application_path=r'H:\SubGameServers\server_v2_netframework\World\bin\Release\net5.0'
    open_exe(application_path+'/World.exe',application_path)
    time.sleep(2)
    # _winapi.CreateProcess(application_path+'/Router.exe',' 18000',None,None,False,_winapi.DETACHED_PROCESS,None,application_path,None)
    # _winapi.SW_HIDE