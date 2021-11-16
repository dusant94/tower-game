import os
import csv
import argparse
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.orm import create_session
from core.orm.models import Beer, BeerStyle

from sqlalchemy import exc
import alembic.config

def check_connection():
    sess = create_session()
    try:
        a = sess.execute("SELECT NOW()")
        return True
    except exc.OperationalError as e:
        return False

if __name__ == '__main__':
    argparser = argparse.ArgumentParser('Simple csv importer')
    argparser.add_argument('--styles', default="storage/csvs/styles.csv")
    argparser.add_argument('--beers', default="storage/csvs/beers.csv")

    args = argparser.parse_args()

    # Wait for connection
    print("Trying to connect to db ...")
    while not check_connection():
        time.sleep(3)
        print("Retrying ...")
    print("Connection succeded !")

    # Check migrations
    alembic.config.main(argv=[
        '--raiseerr',
        'upgrade', 
        'head'
    ])


    # Seed if necessary
    sess = create_session()

    res = sess.execute("SELECT count(*) FROM beers").fetchone()
    count_beers = res[0]

    res = sess.execute("SELECT count(*) FROM beerstyle").fetchone()
    count_styles = res[0]

    if count_styles > 0:
        print(f"Not importing styles, {count_styles} records exist")
    else:
        print(f"Importing styles ({args.styles})...")
        cnt = 0
        with open(args.styles, 'r') as fp:
            creader = csv.DictReader(fp, delimiter=',', quotechar='"')
            for row in creader:
                item = BeerStyle()
                
                item.id = int(row['id'])
                item.name = row['style_name']
                cnt += 1
                sess.add(item)

            sess.commit()
        print(f"Done importing {cnt} styles.")

    if count_beers > 0:
        print(f"Not importing beers, {count_beers} records exist")
    else:
        print(f"Importing beers ({args.beers})...")
        cnt, cntf = 0, 0
        beer_fields = ['name', 'abv', 'ibu', 'srm', 'upc', 'descript', 'last_mod']
        with open(args.beers, 'r') as fp:
            creader = csv.DictReader(fp, delimiter=',', quotechar='"')
            for row in creader:
                # note: not all rows can be processed, there are some artifacts
                #       this is an example app, not going to fix this

                try:
                    item = Beer()
                    item.id = int(row['id'])

                    style_id = int(row['style_id'])
                    
                    if style_id > 0:
                        item.id_style = style_id

                    for fname in beer_fields:
                        setattr(item, fname, row[fname])
                        
                    cnt += 1
                    sess.add(item)
                except:
                    cntf += 1

            sess.commit()
        print(f"Done importing {cnt} beers. (failed {cntf})")