TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ['127.0.0.1',]
if platform.system() == 'Windows':
    NPM_BIN_PATH = r'C:\\Program Files\\nodejs\\npm.cmd'
else:
    NPM_BIN_PATH = '/usr/local/bin/npm'