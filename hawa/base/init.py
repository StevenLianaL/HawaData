from hawa.config import project


def set_project(
        db_host: str = '',
        db_port: int = 3306,
        db_user: str = '',
        db_password: str = '',
        db_name: str = '',
        redis_host: str = '',
        redis_db: int = 0,
        mongo_host: str = '',
        mongo_port: int = 27017,
        mongo_user: str = '',
        mongo_pswd: str = '',
        mongo_db: str = '',
        mongo_auth_db: str = '',
):
    for k, v in vars().items():
        upper_k = k.upper()
        if upper_k in dir(project):
            setattr(project, upper_k, v)
    project.COMPLETED = True
