
import SSH
import os
import configparser

ImitMode = 1

ARMs = {}

if __name__ == '__main__':

    if ImitMode:
        FleName = 'Ssh_exemple.ini'
    else:
        FleName = 'Ssh.ini'

    config = configparser.ConfigParser()

    Ok = 1
    if os.path.exists('Ssh.ini'):
        print('Найден файл ' + FleName + ' идет чтение конфигурации\n')
    else:
        print('Не найден файл ', FleName)
        Ok = 0

    if Ok:
        try:
            with open(FleName) as fp:
                config.read_file(fp)

            # чтение настроек АРМов
            print("Удаленные компьютеры:")
            for key in config['ARMs']:
                ARMs[key] = config['ARMs'][key]
                print(key, ARMs[key])

            # чтение путей для перекладки файла сообщений
            LocalSrs = config['PATH']['Local']
            print('Расположение файла сообщений на локальном компьютере:\n', LocalSrs)
            RemoteSrs = config['PATH']['Remote']
            print('Расположение файла сообщений на удаленном компьютере:\n', RemoteSrs)

            print('Настройки SSH:')
            port = config['SSH']['Port']
            print('Port:', port)
            username = config['SSH']['username']
            print('User:', username)
            password = config['SSH']['password']
            print('password:', password)

            print('команда на перезапуск сервера сообщений:')
            Cmd = config['CMD']['RestartMsg']
            print(Cmd)

            print('')
        except Exception as err:
            Ok = 0
            print("Ошибка конфигурации" + str(err))

    if Ok:
        for ArmName, ArmIp in ARMs.items():
            SSH.RestartMsg(username, port, password, Cmd, ArmName, ArmIp, LocalSrs, RemoteSrs)

    print('\nДля выхода нажмите любую кнопку')
    input()
