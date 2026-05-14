curl -X GET \
  "$HARXITFLOW_URL/api/v1/users/?skip=0&limit=10" \
  -H "accept: application/json" \
  -H "x-api-key: $HARXITFLOW_API_KEY"
