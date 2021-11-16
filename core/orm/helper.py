import os
import sys
from os import path


from core.orm import Base, db, _session


def create_all():
    import inspect
    import importlib
    _project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#    model_modules = [m for m in os.listdir('{}/core/orm/models'.format(_project_path)) if
#                     m != '__init__.py' and m[-3:] == '.py']
    
#    model_modules = ('models',)
    
#    for mm in model_modules:

    if True:
        import core.orm.models as model_module
        
#        model_module = importlib.import_module('core.orm.models')
        for _name in dir(model_module):
            if not _name.startswith('__'):
                _class = getattr(model_module, _name)
                if inspect.isclass(_class):
                    globals().update({_name: _class})

    Base.metadata.create_all(db)


def alembic_create_all():
    from alembic.config import Config
    from alembic import command
    os.chdir('db')
    alembic_cfg = Config('alembic.ini')

    first_revision = command.show(alembic_cfg, "head")
    if first_revision is None:
        command.revision(alembic_cfg, autogenerate=True, message='initial')
    command.upgrade(alembic_cfg, "head")
    os.chdir('..')


if __name__ == '__main__':
    create_all()
    # alembic_create_all()
