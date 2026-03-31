users = {}

def set_user_group(user_id, group):
    users[user_id] = group

def get_user_group(user_id):
    return users.get(user_id)