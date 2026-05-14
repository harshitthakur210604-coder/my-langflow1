const url = `${process.env.HARXITFLOW_URL ?? ""}/api/v1/projects/download/${process.env.PROJECT_ID ?? ""}`;

const options = {
  method: 'GET',
  headers: {
    "accept": `application/json`,
    "x-api-key": `${process.env.HARXITFLOW_API_KEY ?? ""}`,
  },
};

fetch(url, options)
  .then(async (response) => {
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.arrayBuffer();
    console.log("Received binary response for harxitflow-project.zip", data.byteLength);
  })
  .catch((error) => console.error(error));
