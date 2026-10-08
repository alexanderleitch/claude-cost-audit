# Morning briefing

Read-only run. Do not edit files, commit, push, comment, send or create anything.

Write a markdown briefing of at most 300 words for the person who owns this repo:

1. **Code**: run `git fetch`, then list commits on the default branch from the last 24 hours.
   List open PRs waiting for my review (`gh pr list --search "review-requested:@me"`), my own open
   PRs (`gh pr list --author @me`), and failing CI runs on the default branch (`gh run list --limit 5`).
2. **Tickets**: my open, assigned issues (`gh issue list --assignee @me`), or the tracker tools if
   available (Linear, Jira).
3. **Day**: today's meetings and unread email that needs a reply, if a Microsoft 365, Outlook or
   Google connector is available.

If a section's tool is unavailable or not allowed, write one line saying it was skipped. Do not retry.
End with **First 3 things to do**, most urgent first.
