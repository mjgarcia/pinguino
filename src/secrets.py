MYSQL_USERNAME_PATH = '/etc/pinguino/mysql-username'
MYSQL_PASSWORD_PATH = '/etc/pinguino/mysql-password'

GMAIL_SECRETS_FILE = '/etc/pinguino/gmail-client-secrets'
GMAIL_CREDENTIALS_STORE = '/etc/pinguino/credentials'

with open(MYSQL_USERNAME_PATH) as file:
    mysqlUsername = file.read()

with open(MYSQL_PASSWORD_PATH) as file:
    mysqlPassword = file.read()