# Code Style Guide

## Legal
- Always start with `Copyright (c) 2011-2025 Blackrock. All rights reserved.`

## Naming Conventions
- Use `snake_case` for function and variable names.
- Use `CamelCase` for class names.
- Use `UPPER_CASE` for constants.
- Use `_leading_underscore` for internal use variables/functions.

## Type Hints
- Type hints are required for all methods.
- Use Python's built-in types and `typing` module for complex types.
- Example: `def greet(name: str) -> str:`

## Docstrings
- Docstrings must follow the Google format.
- Include descriptions of parameters, return values, and any exceptions raised.
- Example:
  ```python
  def fetch_data(query: str) -> Dict:
      """Fetches data based on the given query.

      Args:
          query: A string representing the data query.

      Returns:
          A dictionary containing the fetched data.

      Raises:
          ValueError: If the query is empty.
      """
