import os


class Settings:
    PROJECT_NAME: str = "FastAPI CSV Reader"
    API_V1_STR: str = "/api"
    CSV_DIR: str = os.path.join(os.getcwd(), "data")


settings = Settings()
