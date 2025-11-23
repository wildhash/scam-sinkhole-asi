# Contributing to ScamSinkhole ASI

Thank you for your interest in contributing to ScamSinkhole! This project aims to combat phone scammers through defensive AI automation.

## Code of Conduct

This project is dedicated to providing a harassment-free experience for everyone. We expect all contributors to:

- Be respectful and professional
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version, etc.)

### Suggesting Features

Feature requests are welcome! Please:
- Check if the feature is already requested
- Clearly describe the feature and its benefits
- Explain how it fits with the project's goals

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**:
   - Follow existing code style
   - Add comments where necessary
   - Update documentation

4. **Test your changes**:
   ```bash
   python demo.py  # Run demo
   python main.py  # Test server
   ```

5. **Commit your changes**:
   ```bash
   git commit -m "Add: brief description of changes"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/wildhash/scam-sinkhole-asi.git
   cd scam-sinkhole-asi
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. Run the demo:
   ```bash
   python demo.py
   ```

## Code Style

- Follow PEP 8 guidelines for Python code
- Use type hints where appropriate
- Write docstrings for classes and functions
- Keep functions focused and single-purpose

Example:
```python
async def example_function(param: str) -> dict:
    """
    Brief description of what the function does.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
    """
    # Implementation
    pass
```

## Project Structure

```
scam-sinkhole-asi/
├── app/
│   ├── core/          # Configuration and models
│   ├── modules/       # Main system modules
│   │   ├── swarm/    # Persona generation
│   │   ├── attack/   # Call management
│   │   ├── intel/    # Intelligence extraction
│   │   └── kill/     # Reporting system
│   ├── api/          # FastAPI endpoints
│   └── ui/           # Web interface
├── main.py           # Application entry point
└── demo.py          # Demonstration script
```

## Module Guidelines

### Swarm Module
Handles AI persona generation and conversation:
- Keep personas diverse and realistic
- Optimize for keeping scammers engaged
- Maintain conversation context

### Attack Module
Manages outbound calls:
- Handle call state properly
- Track metrics accurately
- Implement error handling

### Intel Module
Extracts intelligence from transcripts:
- Balance regex and AI analysis
- Validate extracted data
- Assign confidence scores

### Kill Module
Submits reports to authorities:
- Follow reporting guidelines
- Handle API errors gracefully
- Track submission status

## Testing

Currently, we use the demo script for testing. Future improvements:
- Unit tests for each module
- Integration tests for API
- End-to-end workflow tests

## Documentation

When adding features:
- Update README.md if needed
- Update API.md for API changes
- Add docstrings to new code
- Include usage examples

## Security

- Never commit API keys or secrets
- Use environment variables for configuration
- Validate all user inputs
- Handle errors without exposing sensitive info

## Legal Considerations

All contributors must ensure:
- Code complies with applicable laws
- Features are for defensive purposes only
- No targeting of legitimate businesses
- Respect privacy and consent laws

## Questions?

Feel free to:
- Open an issue for questions
- Join discussions in pull requests
- Reach out to maintainers

## Attribution

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for helping make the internet safer! 🛡️
