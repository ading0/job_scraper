## Intro

Scraper tool + LLM scorer for Otta (Welcome to the Jungle).

## Usage

Install based on requirements.txt.
Two files are excluded by the .gitignore: .env and personal_scoring.py.

.env must have the keys OTTA_EMAIL, OTTA_PASSWORD, and OPENAI_KEY. The first two are used to login to Otta; the last is an OpenAI developer API key (see platform.openai.com).

personal_scoring.py needs a function called "score" of the type ExtractedInfo -> float (or any other type of score).

Then just run main.py.

Results will be output to output/postings.txt
