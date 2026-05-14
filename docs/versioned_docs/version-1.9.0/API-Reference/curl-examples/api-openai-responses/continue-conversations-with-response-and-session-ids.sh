BASE_URL="${HARXITFLOW_SERVER_URL:-$HARXITFLOW_URL}"

curl -X POST \
  "$BASE_URL/api/v1/responses" \
  -H "x-api-key: $HARXITFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "model": "$FLOW_ID",
  "input": "Hello, my name is Alice"
}
EOF
