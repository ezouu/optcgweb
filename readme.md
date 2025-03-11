# OPTCG Web Scraper and Data Collection Tool

## Overview
This project is a comprehensive web scraping and data collection tool specifically designed for the One Piece Trading Card Game (OPTCG). It includes multiple components for gathering card prices, market data, and additional content from various sources.

## Core Features

### 1. OPTCG Card Price Scraper (`scrapertable.py`)
- Automatically scrapes card prices from TCGPlayer for all One Piece Card Game sets
- Supports multiple sets including:
  - Romance Dawn
  - Paramount War
  - Pillars of Strength
  - Kingdoms of Intrigue
  - Awakening of the New Era
  - Wings of the Captain
  - 500 Years in the Future
  - Two Legends
- Collects detailed card information:
  - Card rarity
  - Card number
  - Market price
  - Product URL
  - High-resolution card image URLs
- Stores data in MongoDB for easy access and updates
- Implements retry mechanisms for reliable data collection

### 2. Web Content Scraper (`polscrape2.js`)
- Built with Playwright for modern web scraping
- Handles pagination automatically
- Collects thread content and metadata
- Implements robust error handling and retry logic
- Saves data in structured JSON format

## Technical Requirements

### Dependencies
- Python 3.x
- Node.js
- MongoDB
- Chrome/Chromium browser

### Python Packages
- selenium
- python-dotenv
- pymongo
- requests

### Node.js Packages
- playwright
- fs (built-in)

## Security Features
- Environment variable management for sensitive data
- Headless browser operation support
- Secure MongoDB connection handling

## Performance Features
- Automated retry mechanisms for failed requests
- Configurable delay settings to prevent rate limiting
- Efficient data storage and update mechanisms
- Parallel processing capabilities

## Data Collection Capabilities
- Real-time market price tracking
- High-resolution card image URL collection
- Comprehensive set coverage
- Structured data output in JSON format
- MongoDB integration for persistent storage

## Error Handling
- Robust retry mechanisms for network failures
- Timeout handling for slow responses
- Detailed error logging
- Graceful failure recovery

## Usage Notes
- The system is designed to run autonomously once configured
- Supports both headless and headed browser operations
- Implements rate limiting to respect server requirements
- Automatically handles session management and reconnection

## Technical Architecture
- Modular design for easy maintenance
- Separate components for different data sources
- Configurable parameters for customization
- Scalable database structure

## Future Capabilities
- API endpoint integration
- Real-time price monitoring
- Historical price tracking
- Market trend analysis
- Additional data source integration
