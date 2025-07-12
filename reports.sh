#!/bin/bash
# reports.sh
# This script runs various reports for specified communities.

function display_help() {
	cat << EOF
Description:
  This script runs various reports to process imported data 
  in Savannah for specified communities.

Usage:
  $0 [community id||list of community IDs|all]

Options:
  sll           	  Run reports on all known active communities

Examples
  $0 all
      Goes through each known active community in turn, to run reports.

  $0 1
      Only run reports for community with ID 1.

  $0 1 2 3
      Only run reports for communities with IDs 1, 2, and 3.

EOF
}

function run_report() {
	local report="$1"
	local community="$2"
	echo "$(date '+%Y/%m/%d %H:%M:%S'): Start $report for $community"
	docker exec -it savannah-docker-app-1 python manage.py "$report" --community "$community" >> "$LOGDIR"/"$report"-"$community".log 2>&1
	echo "$(date '+%Y/%m/%d %H:%M:%S'): End $report for $community"
}

function run_all_reports() {
	local community="$1"
	for report in level_check activity_check event_impact gift_impact make_connections make_suggestions make_insights make_reports; do
		run_report "$report" "$community"
	done
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
  # If 'all' is specified, run reports on all communities
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
echo "$(date '+%Y/%m/%d %H:%M:%S'): Start reports"
echo "$(date '+%Y/%m/%d %H:%M:%S'): Start tag_contributions report"
docker exec -it savannah-docker-app-1 python manage.py tag_contributions >> "$LOGDIR"/tag_contributions.log 2>&1
echo "$(date '+%Y/%m/%d %H:%M:%S'): End tag_contributions report"

echo "$(date '+%Y/%m/%d %H:%M:%S'): Start tag_conversations"
docker exec -it savannah-docker-app-1 python manage.py tag_conversations >> "$LOGDIR"/tag_conversations.log 2>&1
echo "$(date '+%Y/%m/%d %H:%M:%S'): End tag_conversations report"

# Loop through each community and run the reports
for community in $communities; do
  run_all_reports "$community"
done
echo "$(date '+%Y/%m/%d %H:%M:%S'): End reports"
