

import paramiko
import os.path
import time

def RestartMsg(username,port,password,Cmd,ArmName,ArmIp,LocalSrs,RemoteSrs):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    Ok = 1
    try:
        print('Подключение по SSH к', ArmName, ArmIp)
        client.connect(hostname=ArmIp, username=username, port=port, password=password, look_for_keys=False,
                       allow_agent=False, timeout=2, banner_timeout=2, auth_timeout=2)
        print('Подключено к', ArmName)
    except Exception as err:
        Ok = 0
        print("Ошибка подключения " + str(err))

    SftpOn = 0
    if Ok:
        try:
            Sftp = client.open_sftp()
            SftpOn = 1
            print('Установлено Sftp соединение с', ArmName)
        except Exception as err:
            Ok = 0
            print("Ошибка установки Sftp соединения " + str(err))

    if Ok:
        if os.path.exists(LocalSrs):
            print('Найден файл ', LocalSrs)
        else:
            print('Не найден файл ', LocalSrs)
            Ok = 0

    if Ok:
        try:
            n=Sftp.put(LocalSrs ,RemoteSrs)
            time.sleep(2)
            print('Файл скопирован на', ArmName, 'в', RemoteSrs )
        except Exception as err:
            Ok = 0
            print("Ошибка копирования файла " + str(err))

    if Ok:
        try:
            print('Выполнение команды', Cmd)
            stdin, stdout, stderr = client.exec_command(timeout=1, command=Cmd)
            time.sleep(2)
            err=stderr.read().decode()
            if str(err)=='':
                print('Сервер сообщений перезапущен на', ArmName)
            else:
                Ok = 0
                print("Ошибка перезапуска сервера сообщений " + str(err))
            print(str(err))
        except Exception as err:
            Ok = 0
            print("Ошибка перезапуска сервера сообщений " + str(err))

    print('')
    if SftpOn:
        Sftp.close()
    client.close()





