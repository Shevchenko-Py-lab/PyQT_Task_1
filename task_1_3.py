from tabulate import tabulate
from task_1_2 import host_range_ping


def host_range_ping_tab():

    res_dict = host_range_ping(True)  # Запрашиваем хосты, проверяем доступность, получаем словарь
    print()
    print(tabulate([res_dict], headers='keys', tablefmt='pipe', stralign='center'))


if __name__ == "__main__":
    host_range_ping_tab()
