curl -X GET \
  "$HARXITFLOW_URL/logs-stream" \
  -H "accept: text/event-stream" \
  -H "x-api-key: $HARXITFLOW_API_KEY"
