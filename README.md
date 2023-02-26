# PokeAPI - Poke-berries statistics API

This project is a technical test that aims to create a Poke-berries statistics API. The API provides endpoints to retrieve various statistics about Poke-berries, including the names of all berries, minimum, maximum, median, variance and mean growth time, as well as the frequency of growth time.

## Getting Started

These instructions will guide you through the process of setting up and running the project on your local machine.

### Prerequisites

To run the project, you will need to have the following software installed on your system:

- Docker
- Docker Compose

## Installation

1. Clone the repository:
`git clone https://github.com/sbontop/globant.git && cd globant/`
2. Install the required packages:
`make build-dev`
3. Set up the environment variables by creating a .env file in the project root directory with the following values:
`touch .env`
And add the following:
DEBUG=True
SECRET_KEY=your-secret-key-here
REDIS_HOST=redis
POKEAPI_URL = "https://pokeapi.co/api/v2/berry"
POKE_API_LIMIT = 100 # limit of items per page
POKE_API_OFFSET = 0 # offset of items per page
POKE_API_CACHE_TIMEOUT = 60 # cache timeout in seconds
4. Run the project:
`make dev` (Run `make prod` in case dev doesn't work)
5. The API is now running and can be accessed at http://localhost:8000/. 
Use the following endpoint to get Poke-berries statistics:
- `curl http://localhost:8000/berry/all_berry_stats/`
To access the plot, open this URL in the browser:
- `http://localhost:8000/berry/plot_growth_time_frequency/`
6. To get a full access to all API Endpoint availables, open the Swagger or Redoc software that display them on the browser:

`http://localhost:8000/api/docs/swagger/`
`http://localhost:8000/api/docs/redoc/`

7. To run the tests, execute the command:

`make test-dev` (Run `make test-prod` if you ran `make prod` above)

## Extra Features

- The use of redis as a cache to speed up the queries.
- A Python library (Matplotlib) to create a histogram graph and display the image in a plain HTML.
- Use Docker to containerize the project

## Authors

- Samuel Braganza (@sbontop)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
