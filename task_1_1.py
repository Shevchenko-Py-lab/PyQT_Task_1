import os
import platform
import subprocess
import threading
from ipaddress import ip_address
from pprint import pprint

result = {'Список доступных узлов': "", 'Список недоступных узлов': ""}

DNULL = open(os.devnull, 'w')


def check_is_ip(value):
    try:
        ipv4 = ip_address(value)
    except ValueError:
        raise Exception('Некорректный ip адрес')
    return ipv4


def ping(ipv4, result, get_list):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    response = subprocess.Popen(["ping", param, '1', '-w', '1', str(ipv4)],
                                stdout=subprocess.PIPE)
    if response.wait() == 0:
        result["Список доступных узлов"] += f"{ipv4} \n "
        res = f"{ipv4} - Узел доступен"
        if not get_list:
            # print(res)
            pass
        return res
    else:
        result["Список недоступных узлов"] += f"{ipv4} \n"
        res = f"{str(ipv4)} - Узел недоступен"
        if not get_list:
            # print(res)
            pass
        return res


def host_ping(hosts_list, get_list=False):
    threads = []
    for host in hosts_list:  # проверяем, является ли значение ip-адресом
        try:
            ipv4 = check_is_ip(host)
        except Exception as e:
            print(f'{host} - {e} - доменное имя')
            ipv4 = host

        thread = threading.Thread(target=ping, args=(ipv4, result, get_list), daemon=True)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if get_list:
        return result


if __name__ == '__main__':
    # список проверяемых хостов
    hosts_list = ['192.168.8.1', '8.8.8.8', 'yandex.ru', 'google.com',
                  '0.0.0.1', '0.0.0.2', '0.0.0.3', '0.0.0.4', '0.0.0.5']
    host_ping(hosts_list)
    pprint(result)
