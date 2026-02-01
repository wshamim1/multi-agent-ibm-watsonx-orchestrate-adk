orchestrate connections set-credentials \
  -a sso-idp-single-exchange-connection-app \
  --env draft \
  --grant-type "urn:ietf:params:oauth:grant-type:token-exchange" \
  --client-id "<client_id>" \
  --token-url "<token_url>"
