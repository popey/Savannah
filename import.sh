#!/bin/bash
# import.sh
# This script imports data into Savannah for specified communities.

function display_help() {
	cat << EOF
Description:
  This script imports data into Savannah for specified communities.

Usage:
  $0 [community id||list of community IDs|all]

Options:
  sll           	  Import data to all known active communities

Examples
  $0 all
      Goes through each known active community in turn, to import.

  $0 1
      Only import data for community with ID 1.

  $0 1 2 3
      Only import data for communities with IDs 1, 2, and 3.

EOF
}

function import_data() {
	local community="$1"
	echo "$(date '+%Y/%m/%d %H:%M:%S'): Start import for $community"
	docker exec -it savannah-docker-app-1 python manage.py import --community "$community" all >> "$LOGDIR"/import-"$community".log 2>&1
	echo "$(date '+%Y/%m/%d %H:%M:%S'): End import for $community"
}

# If no parameters are passed, display the help message
if [ $# -eq 0 ]; then
	display_help
	exit 1
fi

if [[ "$1" == "--help" || "$1" == "-h" ]]; then
	display_help
	exit 1
elif [[ "$1" == "all" ]]; then
  # If 'all' is specified, import all communities
  # But first, discover the communities from the database
  # Source the env file to get POSTGRES_* environment variables
  if [ -f ".env" ]; then
	source ".env"
	export PGPASSWORD="$POSTGRES_PASSWORD"
	communities=$(docker exec -it savannah-docker-db-1 psql -t -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT string_agg(id::text, ' ') FROM corm_community WHERE status = '1';")
	echo $communities
  else
    echo "Error: .env file not found."
	exit
  fi
else
  # If the first argument is not 'all', treat it as a list of community IDs
  # If communities are provided, use that list
  # Validate that the input is a space-separated list of integers
  if ! [[ "$1" =~ ^[0-9]+(\ [0-9]+)*$ ]]; then
	echo "Error: Invalid community IDs. Please provide a space-separated list of integers."
	exit 1
  fi
  # and set the communities variable to that list
  communities="$@"
fi

## Start main loop

DATETIMESTAMP=$(date +%Y.%m.%d.%H.%M)
LOGDIR="$(pwd)/logs/$DATETIMESTAMP"
mkdir -p "$LOGDIR"
echo "$(date '+%Y/%m/%d %H:%M:%S'): Start imports"
# Loop through each community and run the import
for community in $communities; do
	import_data "$community"
done
echo "$(date '+%Y/%m/%d %H:%M:%S'): End imports"
