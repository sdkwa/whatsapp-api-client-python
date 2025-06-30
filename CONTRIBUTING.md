# Contributing to SDKWA WhatsApp API Python SDK

Thank you for your interest in contributing to the SDKWA WhatsApp API Python SDK! We welcome contributions from the community.

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/whatsapp-api-client-python.git
   cd whatsapp-api-client-python
   ```

2. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   ```

## Development Workflow

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the existing code style
   - Update documentation as needed

3. **Run code formatting (optional)**
   ```bash
   # Use dev script for formatting
   python scripts/dev.py format
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

- Follow existing code patterns in the repository
- Use clear, descriptive variable and function names
- Add docstrings to all public functions and classes
- Use type hints for function parameters and return values

## Documentation

- Update the README.md if you add new features
- Add docstrings to all public functions and classes
- Follow the Google docstring style

## Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `chore:` for maintenance tasks

## Pull Request Guidelines

1. **Title**: Use a clear, descriptive title
2. **Description**: Explain what your PR does and why
3. **Documentation**: Update documentation if needed
4. **Breaking Changes**: Clearly document any breaking changes

## Questions?

If you have questions, please:
- Open an issue for discussion
- Check existing issues for similar questions
- Contact the maintainers

Thank you for contributing!
