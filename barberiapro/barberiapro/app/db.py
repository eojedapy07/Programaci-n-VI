from . import models

def init_db():
    # models.ensure_tables already runs on import but keep explicit call
    models.ensure_tables()
