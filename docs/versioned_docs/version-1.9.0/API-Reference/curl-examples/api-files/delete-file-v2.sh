curl -X DELETE \
  "$HARXITFLOW_URL/api/v2/files/$FILE_ID" \
  -H "accept: application/json" \
  -H "x-api-key: $HARXITFLOW_API_KEY"
