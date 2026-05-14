curl -X GET \
  "$HARXITFLOW_URL/api/v1/files/list/$FLOW_ID" \
  -H "accept: application/json" \
  -H "x-api-key: $HARXITFLOW_API_KEY"
