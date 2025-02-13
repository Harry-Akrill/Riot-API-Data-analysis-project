# Riot Games Data Analysis Project

## Overview

This project utilizes the Riot Games Developer API to extract game data for individual players, filters the data based on specific criteria, and imports the processed data into Google Sheets for further analysis.

## Features

Pulls match history and player statistics using the Riot Games API.

Filters and processes the raw data to extract relevant insights.

Automates the export of cleaned data to Google Sheets.

Provides an easy-to-use workflow for tracking player performance.

## Requirements

To run this project, ensure you have the following installed:

Python 3.x

Riot Games Developer API Key

Google Sheets API credentials

Required Python libraries:

pip install requests pandas gspread oauth2client

## Setup

Obtain a Riot Games API Key

Visit the Riot Games Developer Portal.

Sign up or log in to get an API key.

Note that API keys expire periodically, so you may need to refresh it.

Set Up Google Sheets API

Follow the Google Sheets API Quickstart.

Create a Google Cloud project and enable the Google Sheets API.

Download the credentials.json file and place it in the project directory.

Configure Environment Variables

Store your Riot API key and Google Sheets credentials securely.

Example using a .env file:

RIOT_API_KEY=your_api_key_here
GOOGLE_SHEETS_CREDENTIALS=path_to_credentials.json

## Usage

Run the script to fetch and filter data

python main.py

Modify filtering criteria in filter_data.py to refine the dataset.

Check your Google Sheet for the updated data.
