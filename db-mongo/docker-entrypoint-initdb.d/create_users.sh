#!/usr/bin/env bash

function create_user {

    local DATABASE=$1
    local USERNAME=$2
    local PASSWORD=$3

    mongo --username="${MONGO_INITDB_ROOT_USERNAME}" --password="${MONGO_INITDB_ROOT_PASSWORD}" admin<<-EOF
                use ${DATABASE};
				db.createUser({
					user: '${USERNAME}',
					pwd: '${PASSWORD}',
					roles: [ { role: 'readWrite', db: '${DATABASE}' } ]
				})
				EOF
}

create_user $MONGO_INITDB_FLASK_DATABASE $MONGO_INITDB_FLASK_USERNAME $MONGO_INITDB_FLASK_PASSWORD
