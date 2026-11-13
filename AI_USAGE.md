# AI Use Disclosure

## Tools used
Claude (Claude Sonnet 5.5, Anthropic) in a chat conversation.
Conversation link: <(https://claude.ai/share/40620c06-2f8a-41a6-839f-af6bc39b2cfb)>

## What I used it for
- Reading and explaining the assignment requirements and planning the project structure.
- Step-by-step guidance on how to build each module.
- Code for parts of the project (listed below).
- Debugging: finding a missing colon (SyntaxError) in validator.py.

## Which parts of the code were AI-generated or AI-assisted
- validator.py
  - load_airports, and validate_row checks 1-6: Claude gave code outlines
    with blanks and hints; I completed and typed them.
  - parse_datetime, validate_row checks 7-11 (dates, price), to_record:
    code provided by Claude; I typed and tested it.
- csv_loader.py: parse_files was provided by Claude.
- query.py: is_valid_query, matches, run_query, run_queries were provided by Claude.
- flight_parser.py: argparse setup, main, logging, file writing were provided by Claude.

## Key prompts
1. "Read all the requirements, make a structure for the project and tell me
   step by step what to do."
2. "Give me the ready code for each step; I will read it, type it myself
   and learn how it works."
3. Screenshots of terminal errors/output with the question of what is wrong.

## What I changed or verified myself
I typed all the code myself in Codespaces, fixed a syntax error, and tested
each function with my own edge cases (non-ASCII letters, bad dates, nan/inf
prices, equal arrival/departure times, invalid queries). I ran the public
test script: all 29 tests pass.