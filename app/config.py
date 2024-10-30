from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname:str 
    database_port:str 
    database_password:str 
    database_name:str 
    database_username:str 
    secret_Key:str 
    algorithm:str
    access_token_exp_time:int
    
    class Config:
        env_file=".env"
    # api_Key:str
settings=Settings()
