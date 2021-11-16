from random import randint

from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi import Depends
from starlette import responses

import core.orm.models as models

from .dependencies import db
from .models import OutputDefender, DefenderRequest, DefenderResponse
from api import helpers
import random

router = APIRouter()


# Example no db session
@router.get('/', summary="Get some random integers")
def list_random_integers():
    """
    Returns the list of random integers
    """
    return [randint(0, 100) for _ in range(100)]


# Example with db session
@router.get('/', summary="Get some random integers")
def list_defenders_example(*, sess: Session = Depends(db)):
    """
    Returns the list of defenders in example
    """
    defenders = sess.query(models.Defender).all()

    return [OutputDefender.from_orm(defender) for defender in defenders]


@router.post('/defender',
             summary='',
             status_code=201,
             response_model=DefenderResponse)
def create_defender(req: DefenderRequest, db: Session = Depends(db) ):
    round = helpers.pick_round(db)

    tower_id = random.choice([round.hocus_tower_id, round.pocus_tower_id])
    for id in [round.hocus_tower_id, round.pocus_tower_id]:
        if tower_id != id:
            enemy_tower_id = id
    defender = helpers.insert_defender(db, req.nickname, tower_id)
    tower = helpers.get_tower_by_id(db, tower_id)
    enemy_tower = helpers.get_tower_by_id(db, enemy_tower_id)
    resp_dict = dict(id = defender.id,
                    towerName = tower.name,
                    towerHealth = tower.healt,
                    towerDefense = tower.defense,
                    towerDefenders = tower.defender_count,
                    enemyTowerName = enemy_tower.name,
                    enemyTowerHealth = enemy_tower.healt,
                    serverUri = "http://127.0.0.1:999" if tower_id != round.hocus_tower_id else "http://127.0.0.1:666")
 
    return DefenderResponse(**resp_dict)
