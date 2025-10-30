# Contributing to KOO Sentiment Analysis

Thank you for your interest in contributing to the KOO Multilingual Sentiment Analysis project! This document provides guidelines for contributing.

## Ways to Contribute

1. **Bug Reports**: Report bugs through GitHub Issues
2. **Feature Requests**: Suggest new features or improvements
3. **Code Contributions**: Submit pull requests for bug fixes or new features
4. **Documentation**: Improve documentation and examples
5. **Testing**: Help test the tool with different datasets and languages

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/koo-sentiment-analysis.git
   cd koo-sentiment-analysis
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Development Workflow

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test them thoroughly

3. Ensure your code follows the project style:
   - Use meaningful variable and function names
   - Add docstrings to functions and classes
   - Follow PEP 8 style guidelines
   - Add comments for complex logic

4. Test your changes:
   ```bash
   python examples/basic_usage.py
   python examples/analyze_custom_text.py
   ```

5. Commit your changes:
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Create a Pull Request on GitHub

## Code Style Guidelines

### Python Code

- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints where appropriate

Example:

```python
def analyze_sentiment(text: str, language: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyze sentiment of text.

    Args:
        text: Input text to analyze
        language: Language code (optional, will be auto-detected)

    Returns:
        Dictionary with sentiment analysis results
    """
    # Implementation here
    pass
```

### Documentation

- Use clear, concise language
- Include code examples
- Keep README and guides up to date
- Add docstrings to all public functions and classes

### Commit Messages

Use clear, descriptive commit messages:

```
Good:
- "Add support for Punjabi language detection"
- "Fix sentiment score calculation for 3-class models"
- "Update README with installation instructions"

Bad:
- "Fix bug"
- "Update code"
- "Changes"
```

## Testing

Before submitting a pull request:

1. Test with sample data:
   ```bash
   python main.py --mode sample --num-posts 50
   ```

2. Test the dashboard:
   ```bash
   streamlit run src/dashboard/app.py
   ```

3. Run example scripts:
   ```bash
   make test
   ```

4. Test with different languages if your changes affect NLP

## Adding New Features

### Adding a New Language

1. Update `LANGUAGE_NAMES` in `src/utils/language_detector.py`
2. Add Unicode range to `SCRIPT_RANGES` if needed
3. Update `languages` list in `config/config.yaml`
4. Test with sample text in that language

### Adding a New Model

1. Add model identifier to `SUPPORTED_MODELS` in `src/sentiment/multilingual_model.py`
2. Implement sentiment mapping if different from existing models
3. Update documentation
4. Test thoroughly

### Adding New Visualizations

1. Add method to `SentimentCharts` class in `src/visualization/charts.py`
2. Support both static (matplotlib) and interactive (plotly) versions
3. Add to dashboard in `src/dashboard/app.py`
4. Update documentation with example

## Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**:
   - OS and version
   - Python version
   - Package versions
6. **Error Messages**: Full error messages and stack traces
7. **Sample Data**: Minimal example that reproduces the issue

Example bug report:

```markdown
## Bug: Sentiment analysis fails for Telugu text

**Description**
Sentiment analysis throws an error when processing Telugu language posts.

**Steps to Reproduce**
1. Create a post with Telugu text
2. Run sentiment analysis
3. Error occurs

**Error Message**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte...
```

**Environment**
- OS: Ubuntu 20.04
- Python: 3.9.5
- transformers: 4.35.2

**Sample Code**
```python
post = KooPost(
    post_id="1",
    text="తెలుగు వచనం",
    author="user",
    timestamp=datetime.now()
)
analyzer.analyze_post(post)
```
```

## Feature Requests

When requesting features, please include:

1. **Use Case**: Why is this feature needed?
2. **Description**: Detailed description of the feature
3. **Examples**: How would it be used?
4. **Alternatives**: Have you considered alternatives?

## Pull Request Process

1. **Update Documentation**: Update README and relevant docs
2. **Add Tests**: Add or update tests if applicable
3. **Check Style**: Ensure code follows style guidelines
4. **One Feature Per PR**: Keep PRs focused on a single feature or fix
5. **Descriptive PR**: Write a clear description of changes

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
Describe testing done

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No breaking changes
```

## Code Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged
4. Your contribution will be credited

## Questions?

If you have questions:
- Open a GitHub Issue
- Check existing documentation
- Contact maintainers

## Recognition

Contributors will be recognized in:
- README.md
- Release notes
- Project documentation

Thank you for contributing! 🎉
