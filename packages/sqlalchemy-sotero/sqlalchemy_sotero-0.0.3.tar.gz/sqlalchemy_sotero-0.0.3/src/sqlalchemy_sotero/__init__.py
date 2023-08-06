from sqlalchemy.dialects import registry

__version__ = "0.0.3"

registry.register(
    "sotero.postgres", "sqlalchemy_sotero.postgres", "SoteroPGDialect"
)
