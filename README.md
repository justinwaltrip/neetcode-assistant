# Neetcode Assistant

This repository contains the code for a NeetCode assistant. The primary objective of this project is to develop a framework for prompt tuning and evaluation of large language models, focusing on their ability to assist with LeetCode style coding problems. This project aims to leverage the power of AI to provide a more efficient, effective, and user-friendly approach to solving complex coding problems.  A key aspect of this project is the incorporation of the concept of the Zone of Proximal Development (ZPD) to ensure that the AI assistance provided is within the user's range of potential understanding and problem-solving capability.

## Structure

The project is structured as follows:

- `scripts`: Contains the scripts corresponding to stages of the data ingestion process.
- `data`: Contains the data used in the project.

## Getting Started

We use [nix](https://nixos.org/) to make our development environment reproducible. Specifically, we can use the [devenv](https://devenv.sh/) wrapper to automatically create a development environment with all the necessary dependencies. If you don't have devenv installed, follow the instructions [here](https://devenv.sh/getting-started/).

To make it easier to switch between development environments, we can use a separate tool called [direnv](https://direnv.net/). If you don't have direnv installed, follow the instructions [here](https://direnv.net/docs/installation.html). 

After you hook into your shell, you will need to run the command `direnv allow` to allow the `.envrc` file to be loaded into your shell. It will now be automatically loaded and unloaded when you enter and exit the directory.

## Setup

### Ollama

To start Ollama,

```bash
docker compose up -d
```

Once Ollama is running, you can run the following command to download a 5-bit quant of the Mistral 8x7B MOE instruct model,

```bash
docker exec -it neetcode-assistant-ollama-1 ollama run mixtral:8x7b-instruct-v0.1-q5_K_M
```

*Note: This model takes ~32 GB of disk space and requires ~35 GB of RAM to run.*

### Milvus

To start Milvus,

```bash
wget https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh
bash standalone_embed.sh start
rm standalone_embed.sh embedEtcd.yaml
```

## Ingestion Pipeline

- **scrape** - NeetCode 150 problems from their website.
- **download** - subtitles for Youtube solutions to the problems.
- **convert** - WevVTT transcripts to plain text.
- **index** - text for retrieval.
