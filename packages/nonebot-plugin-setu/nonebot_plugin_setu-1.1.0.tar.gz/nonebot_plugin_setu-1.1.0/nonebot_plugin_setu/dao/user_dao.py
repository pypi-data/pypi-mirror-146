import sqlite3
import time
from datetime import datetime
from .group_dao import GroupDao

DEFAULT_GROUP_CD = 3600


class UserDao:
    def __init__(self):
        self.db_path = 'data/lolicon.db'
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            'create table if not exists user_cd(user_id text primary key, last_time integer ,cd integer)')
        self.cursor.execute(
            'create table if not exists r18_private_chat(id integer primary key AUTOINCREMENT, r18 integer default 0)')
        self.conn.commit()
        self.conn.close()
        pass

    @staticmethod
    def datetime_to_seconds(time_obj):
        time_str = time_obj.strftime("%Y-%m-%d %H:%M:%S")
        return int(time.mktime(datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").timetuple()))

    def get_user(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM user_cd WHERE user_id = '{user_id}'")
        user = cursor.fetchone()
        if user is None:
            return None
        data = {}
        for idx, val in enumerate(cursor.description):
            data[val[0]] = user[idx]
        conn.close()
        return data
        pass

    def add_user_cd(self, user_id, last_time, cd):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO user_cd VALUES (?, ?, ?)", (user_id, last_time, cd))
        conn.commit()
        conn.close()
        pass

    def get_user_remain_time(self, user_id, group_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        user = self.get_user(user_id)
        this_time = self.datetime_to_seconds(datetime.now())
        if user is None:
            cd = GroupDao().get_group_cd(group_id)
            if cd is None:
                cd = DEFAULT_GROUP_CD
                GroupDao().set_group_cd(group_id, cd)
            self.add_user_cd(user_id, this_time, -1)
            conn.commit()
            conn.close()
            return 0
        if user['cd'] == -1:
            cd = GroupDao().get_group_cd(group_id)
        else:
            cd = user['cd']
        cursor.execute(f"SELECT last_time FROM user_cd WHERE user_id = '{user_id}'")
        last_time = cursor.fetchone()
        conn.close()
        time_diff = this_time - last_time[0]
        if time_diff >= cd:
            self.update_user_cd(user_id, this_time, '')
            return 0
        else:
            return cd - time_diff
        pass

    def update_user_cd(self, user_id, last_time, cd):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if cd == '':
            cursor.execute(f"UPDATE user_cd SET last_time = '{last_time}' WHERE user_id = '{user_id}'")
        elif last_time == '':
            cursor.execute(f"UPDATE user_cd SET cd = '{cd}' WHERE user_id = '{user_id}'")
        else:
            cursor.execute(f"UPDATE user_cd SET last_time = '{last_time}', cd = '{cd}' WHERE user_id = '{user_id}'")
        conn.commit()
        conn.close()
        pass

    def delete_user_cd(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"UPDATE user_cd SET last_time = '0' WHERE user_id = '{user_id}'")
        conn.commit()
        conn.close()
        pass

    def get_r18_private_chat(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM r18_private_chat WHERE id = 1")
        r18 = cursor.fetchone()
        if r18 is None:
            return 0
        conn.close()
        return r18[1]
        pass

    def set_or_update_r18(self, r18: int = 0):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO r18_private_chat VALUES (?, ?)", (1, r18))
        cursor.execute("UPDATE r18_private_chat SET r18 = '{}' WHERE id = 1".format(r18))
        conn.commit()
        conn.close()
        pass
