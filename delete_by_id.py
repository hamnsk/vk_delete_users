import vk
import os

"""
To use vk.com API you need registered app and login in this social network. vk.com developers guide: https://vk.com/dev/main

1. Sign up in social network.
2. Go to https://vk.com/dev/standalone and create new app. Choose name and select standalone type.
3. Remember app id.
4. Use app id, list of required permissions and user credentials to get access token.
5. Use this access token to make method requests. List of all: https://vk.com/dev/methods. Some methods don’t require access token.
"""

# сюда вставляем свой токен и id группы откуда удаляем

VK_TOKEN = ''
GROUP_ID = 1


def get_auth_api(access_token):
    session = vk.Session(access_token=access_token)
    return vk.API(session)


def read_from_file():
    """
    Файл с id пользователй должен лежать в папке откуда запускается скрипт, название id_list.txt
    :return: строку содержащую id пользователя
    """
    id_file = os.path.join(os.sys.argv[0], 'id_list.txt')
    with open(id_file, 'r'):
        for line in id_file:
            yield line


def main():
    """
    основное тело программы
    для чтения id из файла используем генератор, чтобы меньше кушать памяти

    :return:
    """
    vk_api = get_auth_api(VK_TOKEN)
    group_id = GROUP_ID
    while True:
        id_to_remove = read_from_file()
        if not id_to_remove:
            break
        response = vk_api.groups.removeUser(group_id, id_to_remove)
        if response:
            print('Пользователь {id} успешно удален'.format(id=id_to_remove))
        else:
            print('Возникла ошибка при удалении пользователя: {id}'.format(id=id_to_remove))


if __name__ == '__main__':
    main()
