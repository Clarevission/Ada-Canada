# Optional: let the tracker fill itself (YouTube API, read-only)

**What you get:** `python yt_sync.py week` adds each video's views, engaged views, watch time, average view duration and subscribers gained to `tracker.csv`, and the subscriber count to `channel.csv`.
**What you still copy by hand:** impressions, click-through rate, and the official watch hours from Studio → Earn (the API doesn't provide them). That takes about 2 minutes.
**Safety:** the permission is **read-only**. Google won't let the script upload, edit, delete or comment. Your keys stay in `secrets/`, which git ignores, so they're never shared or committed. Never paste them into a chat.

Time: about 20 minutes, one time. Best done by Clarence with Niqui logged in on the same computer.

## Steps

1. **Create a Google Cloud project.** Go to <https://console.cloud.google.com/>, sign in with the Google account that owns the Ada Canada channel, then **Select a project → New project**. Name it `ada-canada-tracker` → Create.
2. **Turn on two APIs.** Go to **APIs & Services → Library**. Search for and **Enable** both:
   - *YouTube Data API v3*
   - *YouTube Analytics API*
3. **Consent screen.** Go to **APIs & Services → OAuth consent screen** (it may be called "Google Auth Platform → Branding/Audience").
   - User type: **External**. App name: `Ada tracker`. Support email: yours.
   - Under **Audience → Test users**, add the channel's Google account email.
   - You don't need to add scopes here; the script asks for read-only ones itself.
4. **Create the key.** Go to **APIs & Services → Credentials → Create credentials → OAuth client ID**.
   - Application type: **Desktop app**. Name: `ada-desktop` → Create → **Download JSON**.
   - Rename the downloaded file to **`client_secret.json`** and move it into the project's **`secrets/`** folder.
5. **Install the libraries** (in the project folder):
   ```
   pip install google-api-python-client google-auth-oauthlib
   ```
6. **Test it:**
   ```
   python yt_sync.py test
   ```
   A browser opens. Choose the Ada Canada account. Google will warn that the app isn't verified: click **Advanced → Go to Ada tracker (unsafe)**. It's your own app. Allow the two **read-only** permissions. The terminal should print "Connected (read-only) to: Ada Canada".
7. **Weekly use (Sunday):**
   ```
   python yt_sync.py week
   ```
   Then open `tracker.csv` and add impressions and CTR from Studio, open `channel.csv` and replace the watch-hour estimate with the number from Studio → Earn, and run `python weekly.py`.

## Good to know

- **Re-login every 7 days?** While the Google app is in *Testing* mode, logins expire after about a week. The script will just open the browser again. To stop that, go to **OAuth consent screen → Publish app** (it stays private and unverified, which is fine for personal use).
- **Analytics lags 1–3 days.** The script reads up to yesterday.
- **Quota:** a weekly run uses a tiny fraction of the free daily limit.
- **To revoke access at any time:** <https://myaccount.google.com/permissions> → Ada tracker → Remove. Then delete `secrets/token.json`.
- This script is new and hasn't been run against the real channel yet. Do the first run together with Claude, so any surprises get fixed on the spot.
