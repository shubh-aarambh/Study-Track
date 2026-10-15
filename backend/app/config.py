from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "StudyTrack API"
    database_url: str = "postgresql+psycopg://studytrack:studytrack@localhost:5432/studytrack"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
