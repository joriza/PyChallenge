class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = "127.0.0.1"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "secure_pass_here"
    MYSQL_DB = "base_de_datos"


config = {
     "development": DevelopmentConfig
}