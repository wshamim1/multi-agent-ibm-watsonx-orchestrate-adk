orchestrate connections set-credentials -a oauth-auth-code-connection-app \
  --env draft \
  --client-id 'clientid' \
  --client-secret 'clientsecret' \
  --authorization-url 'https://api.example.com/oauth2/authorize' \
  --token-url 'https://api.example.com/oauth2/token' \
  --scope admin
