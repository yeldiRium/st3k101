#!/usr/bin/env bash

mongo --username="${MONGO_INITDB_ROOT_USERNAME}" --password="${MONGO_INITDB_ROOT_PASSWORD}" admin<<-EOJS
                use efla-web;
				db.createUser({
					user: 'flask',
					pwd: 'flask',
					roles: [ { role: 'readWrite', db: 'efla-web' } ]
				})
				EOJS