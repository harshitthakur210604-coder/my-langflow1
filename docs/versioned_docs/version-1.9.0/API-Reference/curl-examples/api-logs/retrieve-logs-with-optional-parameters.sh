curl -X GET \
  "$HARXITFLOW_URL/logs?lines_before=0&lines_after=0&timestamp=0" \
  -H "accept: application/json" \
  -H "x-api-key: $HARXITFLOW_API_KEY"
