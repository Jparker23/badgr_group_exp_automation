# Badgr Automation Tools

A collection of Python scripts for automating common tasks with the Badgr digital badge platform, including badge class management and group expiration date updates.

## Overview

This repository contains four main scripts designed to streamline Badgr administration:

1. **Badge Class Management** - Retrieve and count unique badge classes via API
2. **Group Link Extraction** - Scrape group management links from the web interface
3. **Batch Group Updates** - Update group expiration dates concurrently (high performance)
4. **Sequential Group Updates** - Update group expiration dates one at a time (more stable)

## Scripts

### `get_badge_ids.py`
Connects to the Badgr API to retrieve all badge classes and count unique entities.

**Features:**
- Uses HTTPS connection to Badgr API
- Counts unique badge classes by entityId
- Requires Bearer token authentication

### `get_group_links.py`
Web scrapes the Badgr interface to extract group management links.

**Features:**
- Automated login to Badgr web interface
- Navigates through paginated group listings
- Exports group edit links to CSV file
- Handles up to 100 results per page for efficiency

### `group_date_auto_batch.py`
High-performance batch processing script for updating group expiration dates.

**Features:**
- Concurrent processing (configurable number of simultaneous operations)
- Asynchronous execution for faster processing
- Built-in verification of updates
- Progress tracking and error handling
- Headless browser operation

### `group_date_auto_single.py`
Sequential processing script for updating group expiration dates.

**Features:**
- Single-threaded, stable execution
- Step-by-step processing with detailed logging
- Interactive mode for debugging (headless=False)
- Automatic error detection and pause functionality

## Prerequisites

### Python Dependencies
```bash
pip install playwright
```

### Playwright Browser Setup
```bash
playwright install chromium
```

### Required Credentials
You'll need to configure the following in each script:

1. **Badgr API Token** (for `get_badge_ids.py`)
   - Set the `Bearer` variable with your API token

2. **Badgr Login Credentials** (for web automation scripts)
   - Set `login_email` and `login_password` variables
   - **⚠️ Security Note:** Remove credentials before committing to version control

## Usage

### 1. Get Badge Class Count
```bash
python get_badge_ids.py
```

### 2. Extract Group Links
```bash
python get_group_links.py
```
This creates `group_links.csv` with all group management URLs.

### 3. Update Group Expiration Dates

**For high-volume processing (recommended for 1000+ groups):**
```bash
python group_date_auto_batch.py
```

**For smaller batches or debugging:**
```bash
python group_date_auto_single.py
```

## Configuration

### Expiration Date
Set your desired expiration date in the group update scripts:
```python
new_exp_date = "6/24/2031"  # MM/DD/YYYY format
```

### Concurrent Operations
Adjust the concurrency limit in `group_date_auto_batch.py`:
```python
MAX_CONCURRENT = 20  # Reduce if experiencing timeouts
```

### CSV Output File
Customize the output filename in `get_group_links.py`:
```python
csv_name = "group_links.csv"
```

## Workflow

1. **Extract Group Links**: Run `get_group_links.py` to generate a CSV of all group edit URLs
2. **Update Expiration Dates**: Use either batch or single script to update group expiration dates
3. **Verification**: Both update scripts include built-in verification to ensure changes were applied correctly

## Error Handling

- **Timeouts**: Scripts include timeout handling for slow-loading pages
- **Login Detection**: Automatic re-authentication if session expires
- **Verification**: Date changes are verified after each update
- **Progress Tracking**: Real-time progress reporting with completion percentages

## Security Considerations

- **Never commit credentials** to version control
- Use environment variables or config files for sensitive data
- Consider using Badgr API instead of web scraping when possible
- Review and test scripts in a development environment first

## Troubleshooting

### Common Issues

**Authentication Errors:**
- Verify your Badgr credentials are correct
- Check if your account has necessary permissions
- Ensure API token is valid and not expired

**Timeout Issues:**
- Reduce `MAX_CONCURRENT` value in batch script
- Increase timeout values in script configuration
- Check network connectivity

**Date Format Issues:**
- Ensure date format matches MM/DD/YYYY
- Verify the target date is valid and in the future

### Debug Mode
Set `headless=False` in browser launch options to watch the automation in action:
```python
browser = playwright.chromium.launch(headless=False)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Remove any credentials from code
5. Submit a pull request

## License

This project is provided as-is for educational and administrative purposes. Please ensure compliance with Badgr's terms of service when using these automation tools.

## Disclaimer

These scripts are designed for legitimate administrative use of Badgr platforms. Users are responsible for:
- Complying with Badgr's terms of service
- Ensuring proper authorization before running automation scripts
- Testing scripts in development environments before production use
- Protecting credentials and sensitive data
