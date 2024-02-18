# Neetcode Assistant

This repository contains the code for a NeetCode assistant. The primary objective of this project is to develop a framework for prompt tuning and evaluation of large language models, focusing on their ability to assist with LeetCode style coding problems. This project aims to leverage the power of AI to provide a more efficient, effective, and user-friendly approach to solving complex coding problems.  A key aspect of this project is the incorporation of the concept of the Zone of Proximal Development (ZPD) to ensure that the AI assistance provided is within the user's range of potential understanding and problem-solving capability.

## Structure

The project is structured as follows:

- `scripts`: Contains the scripts corresponding to stages of the data ingestion process.
- `data`: Contains the data used in the project.

## Installation

Pre-conditions:
- [Nix package manager](https://nixos.org/download) is installed.

To enter the development environment, run the following command:

```bash
nix-shell
```

## Stages

- **scrape** - NeetCode 150 problems from their website.
- **download** - Subtitles for Youtube solutions to the problems.
- **convert** - WevVTT to plain text.
