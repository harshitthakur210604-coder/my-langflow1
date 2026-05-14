curl -X GET \
  "$HARXITFLOW_URL/api/v1/projects/download/$PROJECT_ID" \
  -H "accept: application/json" \
  -H "x-api-key: $HARXITFLOW_API_KEY" \
  --output harxitflow-project.zip
