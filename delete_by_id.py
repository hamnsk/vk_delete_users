import vk
import os
import webbrowser
from urllib.parse import parse_qs

"""
To use vk.com API you need registered app and login in this social network. vk.com developers guide: https://vk.com/dev/main

1. Sign up in social network.
2. Go to https://vk.com/dev/standalone and create new app. Choose name and select standalone type.
3. Remember app id.
4. Use app id, list of required permissions and user credentials to get access token.
5. Use this access token to make method requests. List of all: https://vk.com/dev/methods. Some methods don’t require access token.
"""

# сюда вставляем app_id и id группы откуда удаляем

GROUP_ID = 1
APP_ID = 1


def get_auth_params():
    auth_url = ("https://oauth.vk.com/authorize?client_id={app_id}"
                "&scope=groups&redirect_uri=http://oauth.vk.com/blank.html"
                "&display=page&response_type=token&v=5.95".format(app_id=APP_ID))
    webbrowser.open_new_tab(auth_url)
    redirected_url = input("В браузере в адресной строке появилась ссылка, вставьте ее сюда:\n")
    aup = parse_qs(redirected_url)
    aup['access_token'] = aup.pop(
        'https://oauth.vk.com/blank.html#access_token')
    return aup['access_token'][0]


def get_auth_api():
    access_token = get_auth_params()
    session = vk.Session(access_token=access_token)
    return vk.API(session)


def read_from_file():
    """
    Файл с id пользователй должен лежать в папке откуда запускается скрипт, название id_list.txt
    :return: строку содержащую id пользователя
    """
    file = os.path.join(os.path.dirname(os.sys.argv[0]), 'id_list.txt')
    with open(file, 'r') as id_file:
        for line in id_file:
            yield line


def main():
    """
    основное тело программы
    для чтения id из файла используем генератор, чтобы меньше кушать памяти

    :return:
    """
    vk_api = get_auth_api()
    group_id = GROUP_ID
    id_to_remove = read_from_file()
    for user_id in id_to_remove:
        response = vk_api.groups.removeUser(group_id=group_id, user_id=int(user_id), v='5.95')
        if response:
            print('Пользователь {id} успешно удален'.format(id=user_id))
        else:
            print('Возникла ошибка при удалении пользователя: {id}'.format(id=user_id))


if __name__ == '__main__':
    main()
