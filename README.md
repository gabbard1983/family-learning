# Family Learning

Learning apps for the kids, hosted free on GitHub Pages, with progress synced through Supabase.

- `index.html`: home page listing the apps
- `ladybug/`: Ladybug Lab (2nd grade), **built** from `source/ladybug-lab.html`. Don't edit it by hand.
- `config.js`: Supabase project URL and anon key
- `supabase/setup.sql`: the one-time database setup
- `tools/build.py`: rebuilds `ladybug/` from `source/` (`python3 tools/build.py`)

## How sync works
- **Creating the family code:** the first grown-up taps **Grown-ups → Create family sync**. That makes a private family code and a family link.
- **Adding a device:** open the family link once on any device (phones, iPad, Fire tablet). From then on that device syncs on its own.
- **Privacy:** no accounts are needed. Only someone with the family link or code can see or change progress, so treat the link like a house key. The anon key in `config.js` is designed to be public.
- **Nothing gets lost:** stars are counted per device and merged, so devices never overwrite each other. Devices without internet keep working offline and sync later.

## One-time setup (about 20 minutes)

### 1. Supabase (personal account)
1. Sign up at supabase.com with a **personal** email, then click **New project**. Name it `family-learning`, choose region **East US**, and save the database password somewhere safe.
2. Open **SQL Editor → New query**, paste everything in `supabase/setup.sql`, and click **Run**. It should say "Success."
3. Go to **Project Settings → API** and copy the **Project URL** and the **anon public** key. (Never use the `service_role` key here.)

### 2. GitHub Pages
1. Sign up at github.com with a personal email.
2. Create a new repository at github.com/new. Name it `family-learning`, make it **Public** (free Pages needs public), and click **Create repository**.
3. Click **uploading an existing file**, drag in **everything inside** this folder, and click **Commit changes**.
4. Open `config.js` on GitHub, click the ✏️ pencil, paste in the Project URL and anon key, and commit.
5. Go to **Settings → Pages**, set Source to **Deploy from a branch**, choose **main** and **/ (root)**, and click **Save**. After a minute or two, the site is at `https://YOUR-USERNAME.github.io/family-learning/`.

### 3. Turn on sync and add devices
1. Open `https://YOUR-USERNAME.github.io/family-learning/ladybug/` on your phone, then tap **Grown-ups → Create family sync**.
2. Tap **Copy family link** and text it to your wife, or open it on the iPad.
3. **iPhone/iPad:** open the family link in Safari, then tap **Share → Add to Home Screen**.
4. **Fire Kids tablet:** in the Amazon Parent Dashboard, add `https://YOUR-USERNAME.github.io` as an allowed website, then open the family link in her Kids browser.
5. **Moving her current stars over:** in the old Claude version, go to **Grown-ups → Get progress code**. Then type the code into **Grown-ups → Add progress** on the new site.

## Weekly updates
Send Claude the class sheets as usual. Claude updates `source/`, rebuilds, and gives you the changed files (or a pull request, if a GitHub token is set up). Nothing goes live until you upload or merge it.

## Adding the 4th grader's app later
Add `source/<app>.html`, add a `build_app(...)` line in `tools/build.py` with its own folder, and link it from `index.html`. Each app uses its own record (`kid`) under the same family code.
