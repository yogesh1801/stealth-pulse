# Elasticsearch Document Processing and Querying

This project processes a CSV file, indexes the data in Elasticsearch, and performs queries based on a given set of queries.

## Prerequisites

- Python 3.7+
- Docker and Docker Compose
- Git (for cloning the repository)

## File structure
```
project_root/
├── Code/
│   └── elasticsearch.py
├── assessment_data.csv
├── queries.txt              
├── Results/                
└── docker-compose.yml 
└── requirements.txt
```

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yogesh1801/stealth-pulse.git
    cd stealth-pulse
    ```
2. Create and activate a virtual environment(windows) - you will need venv package to do so:
    ```sh
    python -m venv venv
    source venv/Scripts/activate
    ```
3. Install required packages
    ```sh
    pip install -r requirements.txt
    ```
4. start the ES and Kibana contatiners
    ```sh
    docker compose up -d
    ```
5. Run the python script
    ```sh
    cd Code
    python elasticsearch.py
    ```

## Cleaning up  

1. Stop the containers
    ```sh
    docker-compose down
    ```

2. Deactivate the virtual environment
    ```sh
    deactivate
    ```