def authorize(auth,role,role_id):
    try:
        if auth ==True:
            if role==role_id:
                return True
            else:
                return False,'Wrong User'
        else:
            return False,'Not Login'
    except:
        return False,'Not Login'
