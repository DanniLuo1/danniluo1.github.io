# Danni Luo — Personal Website

A minimal, academic-style personal website (inspired by Kaiming He's homepage),
built with plain HTML/CSS and ready to publish on GitHub Pages.

## Preview locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Before publishing

1. **Add your photo** — replace `assets/avatar.svg` with a square photo (e.g. `profile.jpg`)
   and update the `<img>` tag in `index.html`.
2. **Add your LinkedIn link** — search for `TODO` in `index.html` and replace
   the placeholder `href="#"` with your LinkedIn profile URL.
3. **Customize the bio** — adjust the About paragraph in `index.html` to your liking.

## Publish on GitHub Pages

1. Create a new repository on GitHub (e.g. `danni-luo`), without auto-generating a README.
2. Push this folder:

```bash
git init
git add .
git commit -m "Initial personal website"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

3. In the repository: **Settings → Pages → Source** — choose
   `Deploy from a branch`, branch `main`, folder `/ (root)`, and save.
4. Your site will be live at `https://<your-username>.github.io/<repo-name>/`.

For a user/organization site at `https://<your-username>.github.io/`, name the
repository exactly `<your-username>.github.io` and push to `main`.

## Content source

All content comes from Danni Luo's resume. Planned / unverified items from the
resume draft (Atlas, AgentScope, CS336 notes) are intentionally **not** included
until they are completed.
