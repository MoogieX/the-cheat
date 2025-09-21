# Gemini Project Log for "the-cheat"

## V2.0 Feature Idea: Web-based Authentication

**User:** Moogie
**Date:** 2025-09-21

**Concept:** To interact with Google services that require OAuth 2.0 (like Google Docs or Gmail), we can build a web-based authentication flow.

**Proposed Implementation:**
1.  Create a static website using GitHub Pages.
2.  On this website, build a client-side JavaScript application to handle the Google OAuth 2.0 login flow.
3.  The user would log in via the website, which would receive an access token from Google.
4.  The user would then copy this access token from the website and provide it to the local Python script (e.g., by pasting it into the terminal or `config.ini`).
5.  The Python script could then use this token to make API calls to Google services on the user's behalf.

**Status:** Deferred. We will focus on building the core features of the script first (like different AI modes). This will be revisited as a potential "V2.0" feature.
