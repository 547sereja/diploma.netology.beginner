import requests
import time
import json

print('it will take for a while')
token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
user_id = 171691064


class User:
    def __int__(self, user_id, token):
        self.user_id = user_id
        self.token = token

    def get_group(self, user_id, token):
        """
        Функция возвращает множество ID групп пользователя user_id.
        Если не удается получить информацию о пользовате, то возвращается
        пустое множество.
        Параметры:
        user_id : str
            ID пользователя
        token : str
            Токен
        """
        response = requests.get(
            url='https://api.vk.com/method/groups.get',
            params=dict(
                access_token=token,
                v=5.61,
                extended=1,
                user_id=user_id
            )
        )
        user_data = response.json()
        user_groups = set()
        try:
            for items in (user_data['response']['items']):
                user_groups.add(items['id'])
            return user_groups
        except KeyError:
            return user_groups


    def get_friends(self, user_id, token):
        """
        Функция возвращает список ID друзей для пользователя user_id.
        Если не удается получить информацию о пользовате, то возвращается
        пустой список.
        Параметры:
        ----------
        user_id : str
            ID пользователя
        token : str
            Токен
        """
        response = requests.get(
            url='https://api.vk.com/method/friends.get',
            params=dict(
                user_id=user_id,
                access_token=token,
                v=5.61
            )
        )
        try:
            return response.json()['response']['items']
        except KeyError:
            return []


    def get_frinds_group_id(self, user_id, token):
        """
        Функция возвращает множество ID групп друзей для пользователя user_id
        Параметры:
        ----------
        user_id : str
            ID пользователя
        token : str
            Токен
        """
        result = set()
        friends = self.get_friends(user_id, token)
        for k, friend_id in enumerate(friends):
            print(f'Нашли группы {k / len(friends) * 100:.2f} % друзей', end="\r")
            friend_group = self.get_group(friend_id, token)
            result.update(friend_group)
            time.sleep(0.4)
        print(f'Нашли группы 100 % друзей', end="\r")
        return result




    # Если было введено username, то преобразуем его в user_id
    response = requests.get(
        url='https://api.vk.com/method/users.get',
        params=dict(
            user_ids=user_id,
            access_token=token,
            v=5.61,
        )
    )
    user_id = response.json()['response'][0]['id']

    def groups_data(self):
        # Считываем данные о группах
        user_group = self.get_group(user_id, token)
        user_frinds_group = self.get_frinds_group_id(user_id, token)
        unique_group = user_group - user_frinds_group

        # Записываем json файл
        result = []
        for k, group in enumerate(unique_group):
            # Получаем информацию об уникальных группах пользователя
            response = requests.get(
                url='https://api.vk.com/method/groups.getById',
                params=dict(
                    group_id=group,
                    access_token=token,
                    v=5.61,
                    fields='members_count'
                )
            )
            response = response.json()['response'][0]
            if 'members_count' in response.keys():
                members_count = response['members_count']
            else:
                members_count = 'Не известно'
            result.append(
                dict(
                    name=response['name'],
                    gid=response['id'],
                    members_count=members_count
                )
            )
            time.sleep(0.4)
            print(
                f'Нашли информацию о {k/len(unique_group)*100:.2f} % уникальных группах',
                end="\r"
            )
            return result

        with open('groups.json', 'w') as foud:
            json.dump(result, foud, ensure_ascii=True, indent=4)

