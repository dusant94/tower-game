from sqlalchemy.orm import Session, exc
from core.orm.models import Round, Defender, Tower
from datetime import datetime as dt
from core.orm import create_session


def insert_defender(db: Session, nickname: str, tower_id):
    defender = Defender(nickname=nickname,
                        attack_points_generated=500,
                        defense_points_generated=500,
                        tower_id=tower_id)

    db.add(defender)
    db.commit()
    db.refresh(defender)

    return defender

def pick_round(db: Session):
    round = db.query(Round).order_by(Round.id.desc()).first()
    if round is not None:
        return round 
    else:
        round = create_round(db)
        return round


def get_tower_by_id(db: Session, id):
    tower_obj = db.query(Tower)\
    .filter(Tower.id == id)\
    .one_or_none()
    return tower_obj

    
def create_round(db):

    round = Round(global_defender_count=0)
                
    db.add(round)
    db.commit()
    db.refresh(round)

    hocus_tower = create_tower(db,"Hocus", round.id)
    pocus_tower = create_tower(db, "Pocus", round.id)
    round.hocus_tower = hocus_tower
    round.pocus_tower = pocus_tower

    db.commit()
    db.refresh(round)

    return round

def create_tower(db, name, round_id):
    tower = Tower(healt=5000,
                  defense=1000,
                  defender_count=0,
                  round_id=round_id,
                  name=name
                  )
                   
    db.add(tower)
    db.commit()
    db.refresh(tower)

    return tower

def add_tower_points(id):
    db = create_session()
    defender = db.query(Defender)\
    .filter(Defender.id == id)\
    .one_or_none()
    tower_id = defender.tower_id

    tower_obj = db.query(Tower)\
    .filter(Tower.id == tower_id)\
    .one_or_none()
    round_id = tower_obj.round_id

    round = db.query(Round)\
    .filter(Round.id == round_id)\
    .one_or_none()
    round.hocus_tower.healt = round.hocus_tower.healt + 1000
    round.pocus_tower.healt = round.pocus_tower.healt + 1000
    
    db.commit()
    return round.hocus_tower, round.pocus_tower
