const url = `${process.env.HARXITFLOW_SERVER_URL ?? ""}/api/v1/responses`;

const options = {
  method: 'POST',
  headers: {
    "x-api-key": `${process.env.HARXITFLOW_API_KEY ?? ""}`,
    "Content-Type": `application/json`,
    "X-HARXITFLOW-GLOBAL-VAR-OPENAI_API_KEY": `sk-...`,
    "X-HARXITFLOW-GLOBAL-VAR-USER_ID": `user123`,
    "X-HARXITFLOW-GLOBAL-VAR-ENVIRONMENT": `production`,
  },
  body: JSON.stringify({
  "model": "your-flow-id",
  "input": "Hello"
}),
};

fetch(url, options)
  .then(async (response) => {
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const text = await response.text();
    console.log(text);
  })
  .catch((error) => console.error(error));
