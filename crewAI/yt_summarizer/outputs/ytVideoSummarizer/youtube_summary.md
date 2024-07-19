**SUMMARY**

Host: Not specified
Topic: Instagram Basic Display API Tutorial

**IDEAS**

- Instagram Basic Display API allows access to user data.
- Requires specific user permissions (e.g., profile, media).
- Authorization process involves obtaining authorization code.
- Authorization code is exchanged for access token.
- Access token used to make API calls.
- API calls return user information (e.g., ID, username).
- Instagram Graph API used for non-data-reading purposes.
- App must be in consumer type, not business type.
- Facebook Client App must be created to integrate API.
- Instagram app must be created within Facebook app.
- Instagram tester role assigned to user for testing.
- Instagram app status can be changed from development to live.
- Authorization API call obtains authorization code.
- Access token endpoint used to exchange code for access token.
- Response includes access token and user ID.
- API call endpoint accepts access token as parameter.
- API call returns user ID and username as response.

**INSIGHTS**

- Instagram Basic Display API grants read-only access to user data.
- OAuth 2.0 protocol used for authentication.
- Authorization and access token process ensures secure API access.
- Tester role allows testing of API functionality.
- Live mode requires app review and approval.
- API calls return essential user information.
- Facebook developers website provides comprehensive API documentation.

**QUOTES**

- "Primary purpose of Instagram Basic Display API is to provide users data."
- "Instagram basic display API basically provide read access of the data."
- "Any of the Instagram display API will need or will use that access local as an authentication."
- "You can either select consumer or any of the type."
- "In order to implement Instagram basic display API we have to create an Instagram app."
- "Instagram 9 is in Dev mode we will not be able to test this particular thing on any of the actual Instagram account any public account."
- "Once we accepted the invitation of Instagram tester from our Instagram account this pending symbol no longer exists."
- "We queried that particular endpoint and we got the response a successful response is actually returning the ID user ID and the username of the user."

**HABITS**

- Using browsers for direct API calls.
- Utilizing curl requests from terminal for API calls.

**FACTS**

- Authorization code and access token have a validity of 1 hour.
- Long-lived access tokens have a validity of 60 days.
- Redirect URI provides the endpoint for authorization.
- De-authorized URI specifies the endpoint for denying authorization.
- Data deletion URL allows users to request data removal.

**REFERENCES**

- Facebook developers website
- Instagram Basic Display API documentation

**ONE-SENTENCE TAKEAWAY**

Follow the steps in this tutorial to successfully use Instagram Basic Display API to access user data.

**RECOMMENDATIONS**

- Explore the Facebook developers website for detailed API information.
- Follow the authorization process carefully to obtain the required tokens.
- Test the API functionality using the Instagram tester role.
- Use the appropriate endpoints for different API calls.
- Keep track of token validity and refresh as necessary.