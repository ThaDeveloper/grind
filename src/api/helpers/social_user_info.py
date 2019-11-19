def get_user_info(user):
    return {
        'email': user.get('email'),
        'first_name': user.get('name').split(' ')[0],
        'last_name': user.get('name').split(' ')[1]
    }
