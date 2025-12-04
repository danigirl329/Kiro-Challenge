---
inclusion: always
---

# Code Quality Standards

## General Principles

When writing or reviewing code, always prioritize:

1. **Readability**: Code should be easy to understand
2. **Maintainability**: Code should be easy to modify and extend
3. **Reliability**: Code should handle errors gracefully
4. **Performance**: Code should be efficient but not prematurely optimized
5. **Security**: Code should follow security best practices

## Python Code Standards

### Style and Formatting
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Keep functions small and focused (single responsibility)
- Add docstrings to functions and classes
- Use type hints for function parameters and return values

### Error Handling
- Use try-except blocks for operations that can fail
- Catch specific exceptions, not bare `except:`
- Log errors with appropriate context
- Provide helpful error messages to users
- Clean up resources in finally blocks or use context managers

### Best Practices
- Use list comprehensions for simple transformations
- Prefer f-strings for string formatting
- Use `with` statements for file and resource handling
- Avoid mutable default arguments
- Use `pathlib` for file path operations

## TypeScript/JavaScript Standards

### Style and Formatting
- Use consistent indentation (2 or 4 spaces)
- Use meaningful variable and function names
- Prefer `const` over `let`, avoid `var`
- Use arrow functions for callbacks
- Add JSDoc comments for complex functions

### Type Safety
- Use TypeScript for type safety
- Define interfaces for data structures
- Avoid `any` type when possible
- Use union types and type guards appropriately

### Best Practices
- Use async/await instead of promise chains
- Handle promise rejections
- Use optional chaining (`?.`) and nullish coalescing (`??`)
- Destructure objects and arrays for cleaner code
- Use template literals for string interpolation

## AWS CDK Standards

### Infrastructure as Code
- Use descriptive construct IDs
- Group related resources in constructs
- Use environment variables for configuration
- Add CloudFormation outputs for important values
- Use removal policies appropriately (DESTROY for dev, RETAIN for prod)

### Security
- Follow principle of least privilege for IAM roles
- Enable encryption at rest and in transit
- Use VPCs and security groups appropriately
- Don't hardcode secrets or credentials
- Use AWS Secrets Manager or Parameter Store

### Best Practices
- Use CDK constructs at appropriate levels (L1, L2, L3)
- Leverage AWS Solutions Constructs when available
- Add tags for resource organization
- Use CDK context for environment-specific configuration
- Test infrastructure code before deployment

## Testing Standards

### Unit Tests
- Test individual functions and methods
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Mock external dependencies
- Aim for high code coverage

### Integration Tests
- Test interactions between components
- Use realistic test data
- Clean up test resources after tests
- Test error scenarios and edge cases

## Git Commit Standards

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb in present tense (Add, Fix, Update, Remove)
- Keep first line under 50 characters
- Add detailed description if needed
- Reference issue numbers when applicable

### Commit Organization
- Make atomic commits (one logical change per commit)
- Don't commit commented-out code
- Don't commit sensitive information
- Review changes before committing

## Documentation Standards

### Code Comments
- Explain "why", not "what" (code should be self-explanatory)
- Update comments when code changes
- Remove outdated or misleading comments
- Use TODO comments for future improvements

### README Files
- Include project overview and purpose
- Provide setup and installation instructions
- Document environment variables and configuration
- Include usage examples
- Add troubleshooting section

### API Documentation
- Document all endpoints with descriptions
- Include request/response examples
- Document authentication requirements
- Specify required vs optional parameters
- Keep documentation in sync with code

## Security Best Practices

### Credentials and Secrets
- Never commit credentials or API keys
- Use environment variables for sensitive data
- Use AWS Secrets Manager for production secrets
- Rotate credentials regularly
- Use IAM roles instead of access keys when possible

### Input Validation
- Validate all user input
- Sanitize data before using in queries
- Use parameterized queries to prevent injection
- Implement rate limiting for APIs
- Validate file uploads (type, size, content)

### Dependencies
- Keep dependencies up to date
- Review security advisories
- Use lock files (package-lock.json, requirements.txt)
- Audit dependencies for vulnerabilities
- Remove unused dependencies

## Performance Considerations

### Optimization
- Profile before optimizing
- Focus on algorithmic improvements first
- Cache expensive operations when appropriate
- Use pagination for large datasets
- Implement lazy loading when beneficial

### Database
- Use indexes for frequently queried fields
- Avoid N+1 query problems
- Use connection pooling
- Implement query timeouts
- Monitor slow queries

### API Design
- Implement caching headers
- Use compression for responses
- Implement rate limiting
- Return only necessary data
- Use async operations for long-running tasks

## Code Review Checklist

Before submitting code:
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New code has tests
- [ ] Documentation is updated
- [ ] No sensitive data in code
- [ ] Error handling is implemented
- [ ] Code is readable and maintainable
- [ ] Performance is acceptable
- [ ] Security best practices followed
