from V1 import app

#Debug should be false in production

app.DEBUG = True
app.SECRET_KEY = 'cbbfvfjjfjjjfsjajjkkvsjh4636787531r9898298981'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False