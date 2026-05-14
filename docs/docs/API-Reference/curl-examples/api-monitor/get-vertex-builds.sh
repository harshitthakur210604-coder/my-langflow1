curl -X GET \
  "$HARXITFLOW_URL/api/v1/monitor/builds?flow_id=$FLOW_ID" \
  -H "accept: application/json" \
  -H "x-api-key: $HARXITFLOW_API_KEY"
