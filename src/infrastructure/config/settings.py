from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="TODOLIST",       # TODOLIST_DATABASE_URL sobrescreve settings.database_url
    settings_file=["settings.toml", ".secrets.toml"],
    environments=False,              # habilita seções [development], [production], etc.
    env_switcher="ENV_FOR_DYNACONF",
    load_dotenv=True,               # lê .env se existir (útil para CI/CD)
    dotenv_path=".env",
)

def get_database_url() -> str:
    url: str = settings.DATABASE_URL
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    return url
