curl -X POST \
  "$HARXITFLOW_SERVER_URL/api/v1/webhook/$FLOW_ID" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $HARXITFLOW_API_KEY" \
  -d '{"data": "example-data"}'
