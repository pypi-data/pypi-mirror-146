# Influence API

A python API for [Influence](https://influenceth.io).

## Development

You **must** have an API key from Influence to develop or use the API. Contact `DarkosNightmare#8555` on Discord, and request a production API key.

The preferred development environment is GitPod.

You will need the following environment variables defined to run unit tests:

- `INFLUENCE_CLIENT_ID`
- `INFLUENCE_CLIENT_SECRET`

Otherwise, tests relying on the live API will be skipped.

## Usage

```python
from influence_api import InfluenceClient

client = InfluenceClient()

assert influence_client.get_asteroid(1)["name"] == "TG-29980 'Adalia Prime'"

assert influence_client.get_crewmate(1)["name"] == "Scott Manley"
```
