# LangSmith Traccia AI Agent Monitoring

This Python script demonstrates how to monitor AI agents in production using LangSmith for observability. It simulates an AI agent that can produce unexpected outputs and logs these interactions, including potential errors, to LangSmith. It also includes a conceptual simulation of Traccia's enforcement approach by checking responses against predefined rules.

## Language

`python`

## How to Run

1. Install LangSmith: `pip install langsmith`
2. Set your LangSmith API key as an environment variable: `export LANGSMITH_API_KEY='YOUR_API_KEY'`
3. Run the script: `python agent_monitoring.py`

## Original Article

This example accompanies the Turkish article: [LangSmith vs Traccia: Üretimdeki Yapay Zeka Ajanları](https://fatihsoysal.com/blog/langsmith-vs-traccia-uretimdeki-yapay-zeka-ajanlari/).

## License

MIT — see [LICENSE](LICENSE).
