curl -X POST \
  "$HARXITFLOW_SERVER_URL/api/v1/responses" \
  -H "x-api-key: $HARXITFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-HARXITFLOW-GLOBAL-VAR-OPENAI_API_KEY: sk-..." \
  -H "X-HARXITFLOW-GLOBAL-VAR-USER_ID: user123" \
  -H "X-HARXITFLOW-GLOBAL-VAR-ENVIRONMENT: production" \
  -d '{
    "model": "your-flow-id",
    "input": "Hello"
  }'
