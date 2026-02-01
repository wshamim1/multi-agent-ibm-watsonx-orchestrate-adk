orchestrate connections set-identity-provider --app-id sso-idp-flow-connection-app \
  --env draft \
  --url https://idp-server/oauth2/v2.0/token \
  --client-id clientid \
  --client-secret clientsecret \
  --scope scope \
  --grant-type urn:ietf:params:oauth:grant-type:jwt-bearer
