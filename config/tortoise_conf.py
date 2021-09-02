TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["src.models.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}