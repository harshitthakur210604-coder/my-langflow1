FROM harxitflowai/harxitflow:1.0-alpha

CMD ["python", "-m", "harxitflow", "run", "--host", "0.0.0.0", "--port", "7860"]
