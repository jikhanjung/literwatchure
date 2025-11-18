# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Literwatchure is a Literary Clock web application that displays the current time using quotes from classic literature where time is mentioned. It extracts time-referenced sentences from Project Gutenberg books and displays them in a React web app.

Example: If the current time is 3:00 PM, it might display "The clock struck three o'clock, and I heard him walk to the door." (Wuthering Heights, Emily Brontë)

## Architecture

### Two-Part System

1. **Data Collection Pipeline (Python)**: Downloads books from Project Gutenberg, extracts time-referenced sentences, and generates `public/times.json`
2. **Web Application (React + Vite)**: Displays current time with matching literary quotes

### Data Flow

```
Project Gutenberg → download_books.py → books/*.txt → extract_times.py → public/times.json → React App
```

### Key Components

**Python Scripts (data-collection/)**:
- `download_books.py`: Downloads books from Project Gutenberg using `books_list.json`, respects `excluded_books.json`, handles rate limiting and 403 errors
- `extract_times.py`: Extracts time patterns from downloaded books using regex (12 different patterns including "3:00", "three o'clock", "half past four", "midnight", "noon"), outputs to `public/times.json`
- `check_coverage.py`: Analyzes coverage of the 1440 possible time slots (00:00-23:59), generates `covered_times.txt` and `missing_times.txt`
- `remove_book.py`: Utility to remove quotes from a specific book from `times.json`

**React App (src/)**:
- `App.jsx`: Main component managing time updates and quote selection, implements fallback logic to find closest available time when exact match doesn't exist
- `components/Clock.jsx`: Displays current time
- `components/Quote.jsx`: Displays literary quote with book metadata

### Data Structures

**times.json format**:
```json
{
  "09:13": [
    {
      "quote": "At nine thirteen, the clock struck.",
      "title": "Example Book",
      "author": "Example Author",
      "position": 45.2
    }
  ]
}
```

**books_metadata.json**: Contains list of downloaded books with `extracted` flag to track processing status

**excluded_books.json**: Books to exclude from processing (religious texts, technical manuals, non-English books)

## Development Commands

### Web Application

```bash
# Install dependencies
npm install

# Run development server (http://localhost:5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Data Collection

```bash
# Navigate to data-collection directory
cd data-collection

# Install Python dependencies
pip install -r requirements.txt

# Download books from Project Gutenberg
python download_books.py

# Extract time sentences and generate times.json
python extract_times.py

# Check coverage statistics
python check_coverage.py

# Remove specific book from times.json
# Edit remove_book.py to set the book title, then run:
python remove_book.py
```

## Important Patterns and Behaviors

### Time Extraction Patterns

The `extract_times.py` script recognizes 12 different time patterns:
1. Numeric with colon: "3:45", "10:30 PM"
2. Word + o'clock: "three o'clock"
3. Fraction past: "half past three", "quarter past four"
4. Quarter to: "quarter to four"
5. Special words: "midnight" (00:00), "noon" (12:00)
7-10. Various "X past/to Y" patterns with minutes
11-12. Numeric combinations with context validation

Sentences are limited to 250 characters to ensure quotes are concise and readable.

### Data Quality Management

The project maintains data quality through:
- **excluded_books.json**: Maintains a list of books to exclude (religious texts, technical manuals, misclassified books)
- **Metadata tracking**: `extracted` flag prevents re-processing books
- **Incremental processing**: `extract_times.py` loads existing `times.json` and only processes new books
- **devlog/**: Contains detailed logs of data cleanup operations (see `2025-01-18-data-cleanup.md` for example)

**Important**: Project Gutenberg metadata can be unreliable. Some books have been misclassified (e.g., ID 10900 was labeled as "Moralia" but was actually King James Bible). Always verify book content when adding new books.

### Download Script Safeguards

- **Rate limiting**: 5-8 second random delay between downloads
- **403 error handling**: Stops after 10 consecutive 403 errors to avoid IP bans
- **Retry logic**: Up to 3 retries for failed downloads
- **Error logging**: Records all download failures to `download_errors.log`
- **Exclusion checking**: Filters books before downloading using `excluded_books.json`

### React App Quote Selection Logic

1. If exact time match exists in `times.json`, use it (random selection if multiple quotes)
2. Otherwise, find closest available time using circular distance calculation (accounting for 24-hour wraparound)
3. Prevents quote flicker by only changing quotes when:
   - Minute changes, OR
   - 10+ seconds elapsed since last change, OR
   - First load

## File Structure

```
literwatchure/
├── data-collection/           # Python data pipeline
│   ├── books/                 # Downloaded book texts (.txt files)
│   ├── books_list.json        # Master list of Project Gutenberg book IDs
│   ├── books_metadata.json    # Metadata with extraction status
│   ├── excluded_books.json    # Books to exclude from processing
│   ├── download_books.py
│   ├── extract_times.py
│   ├── check_coverage.py
│   ├── remove_book.py
│   └── requirements.txt
├── src/                       # React application
│   ├── components/
│   │   ├── Clock.jsx
│   │   └── Quote.jsx
│   ├── App.jsx
│   └── App.css
├── public/
│   └── times.json            # Generated time quotes data
├── devlog/                   # Development logs and cleanup records
├── package.json
└── vite.config.js
```

## Technology Stack

- **Frontend**: React 18 + Vite 5
- **Styling**: Vanilla CSS3 with dark mode support
- **Data Collection**: Python 3.8+ with requests, beautifulsoup4, gutenbergpy
- **Data Source**: Project Gutenberg (https://www.gutenberg.org/)

## Coverage Information

As of the latest data cleanup (see `devlog/2025-01-18-data-cleanup.md`):
- Coverage: ~39.2% of 1440 possible time slots
- Total quotes: 16,193 from 987 books
- Quality focus: Only literary works, no religious texts or technical manuals

Run `python check_coverage.py` for current statistics and to generate updated `covered_times.txt` and `missing_times.txt` files.
