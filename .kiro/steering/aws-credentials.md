---
inclusion: always
---

# AWS Credentials Management

## Important: Terminal and Credentials

When running AWS CLI commands, be aware that:

1. **Terminal Sessions**: Each new terminal session may not have AWS credentials configured
2. **Environment Variables**: AWS credentials are often set via environment variables that don't persist across terminal sessions
3. **Credential Verification**: Always verify credentials are available before running AWS commands

## Before Running AWS Commands

Before executing any AWS CLI commands, check if credentials are available:

```bash
aws sts get-caller-identity
```

If this command fails, the user needs to configure credentials.

## When Credentials Are Missing

If AWS commands fail with authentication errors:

1. **Prompt the user** to configure their AWS credentials
2. **Ask if they need help** setting up credentials
3. **Suggest options**:
   - Run `aws configure` to set up credentials
   - Set environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)
   - Use AWS SSO login if applicable
   - Check if credentials have expired

## Common Credential Issues

- **Session tokens expired**: Temporary credentials need to be refreshed
- **Wrong profile**: User may need to specify `--profile` flag
- **Region not set**: Some commands require explicit region configuration
- **Permissions**: User may not have necessary IAM permissions

## Best Practices

- **Don't assume credentials are available** - always verify first
- **Provide helpful error messages** when credential issues occur
- **Suggest specific solutions** based on the error message
- **Never expose or log** credential values
- **Remind users** to keep credentials secure

## Example Workflow

When a user asks to run AWS commands:

1. First, check if credentials work: `aws sts get-caller-identity`
2. If successful, proceed with the requested command
3. If failed, inform the user and provide guidance on setting up credentials
4. After credentials are configured, retry the original command
