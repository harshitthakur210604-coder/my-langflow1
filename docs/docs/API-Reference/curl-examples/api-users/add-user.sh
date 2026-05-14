curl -X POST \
  "$HARXITFLOW_URL/api/v1/users/" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $HARXITFLOW_API_KEY" \
  -d '{
    "username": "newuser2",
    "password": "securepassword123"
  }'
