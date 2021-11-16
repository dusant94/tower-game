#!/bin/sh

echo "This will remove: 
    - alembic revision
    - seed files
    - beer router
    - beer models from orm/models.py
    - this file ($0)"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_DIR="$( dirname "${SCRIPT_DIR}" )"

echo
echo -e "Project directory:\n\t ${PROJECT_DIR}"
echo
read -p "Press enter to continue (check project directory !)"

echo "Changing workdir to ${PROJECT_DIR}"
cd "${PROJECT_DIR}"

echo "Removing revisions ..."
rm -v alembic/versions/*

echo "Cleaning uncessary files ..."
rm -rv storage/csvs

echo "Removing beer router ..."
rm -v api/beers.py
IMP_LINE="$( awk '/import beers/{ print NR; exit}' main.py )"
INCL_LINE="$(($( awk '/beers.router,/{ print NR; exit}' main.py )-2))"
INC_END_LINE=$((${INCL_LINE}+4))
sed -i "${IMP_LINE}d" main.py
sed -i "${INCL_LINE},${INC_END_LINE}d" main.py

echo "Cleaning models.py ..."
BEER_LINE="$(awk '/class Beer/{ print NR; exit}' core/orm/models.py)"
sed -i "${BEER_LINE},\$d" core/orm/models.py

echo "Cleaining dbinit.py ..."
IMP_LINE_M="$( awk '/from core.orm.models import Beer/{ print NR; exit}' tools/dbinit.py )"
sed -i "${IMP_LINE_M}d" tools/dbinit.py
SEL_LINE="$( awk '/res = sess.execute\("SELECT count/{ print NR; exit}' tools/dbinit.py )"
sed -i "${SEL_LINE},\$d" tools/dbinit.py

echo "Done."
echo

echo 
echo "To create initial (and subsequent) revision do: 

    cp storage/config_templates/docker/db.yaml storage/config/

    # Change host param to \"localhost\" 
    sed -i 's/psql/localhost/g' storage/config/db.yaml

    # Add necessary models in orm/models.py

    # Run the postgres db in background
    docker-compose up -d pgmaster

    # NOTE: the NAME param if you want to name the revision
    make alembic-revision NAME=\"name-of-my-revision\"
    
    # Stop the postgres container
    docker-compose stop
    
    # Test it
    docker-compose down -v
    docker-compose up --build
    
    # Done !
"

read -p "Press enter to remove this script ($0)"
rm -- "$0"
