# DAS API

This directory contains templates and skeleton frameworks for data and configurations used in the Data Aggregator and Server (DAS) API of the DashAR system.

## Templates

### dashar-data.sqlite3

This SQLite3 Database is used to store runtime data of the DashAR system, as data is being collected from the various sources (OBDII, third-party APIs, etc.). This specific file is only the database structure used by the system. To use it, copy this file to the "Source/DAS/private/" directory.

### config.json

This collection of JSON files define the behavior of the DAS API. These include an examples of config.json files, as well as schema definitions (e.g. config.schema.json).
