# Setting Up Your GitHub Repository

Follow these steps to publish your port scanner to GitHub.

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `port-scanner` (or your preferred name)
3. Description: "Fast multithreaded Python port scanner for network reconnaissance"
4. Choose: Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Initialize Local Repository

Open terminal in the `port-scanner-repo` directory and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Port Scanner v1.0"

# Rename branch to main (if needed)
git branch -M main
```

## Step 3: Connect to GitHub

Replace `YOUR-USERNAME` with your actual GitHub username:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR-USERNAME/port-scanner.git

# Push to GitHub
git push -u origin main
```

## Step 4: Update README Links

After pushing, update these files to replace `YOUR-USERNAME` with your actual username:

- `README.md` (line with GitHub clone URL)
- `docs/INSTALL.md` (clone instructions)
- `SECURITY.md` (if you added email)

Then commit and push the changes:

```bash
git add README.md docs/INSTALL.md SECURITY.md
git commit -m "Update repository links"
git push
```

## Step 5: Configure Repository Settings

On GitHub, go to your repository settings:

### Topics
Add relevant topics to help people find your project:
- `python`
- `security`
- `networking`
- `port-scanner`
- `penetration-testing`
- `cybersecurity`
- `network-security`

### About Section
Edit the "About" section (top right of repo page):
- Description: "Fast multithreaded Python port scanner for network reconnaissance"
- Website: (optional - your portfolio site)
- Topics: Add the topics above

### GitHub Pages (Optional)
If you want documentation hosted:
1. Go to Settings > Pages
2. Source: Deploy from branch
3. Branch: main, folder: /docs

## Step 6: Enable GitHub Actions

The CI/CD workflow should automatically run when you push. Check the "Actions" tab.

## Step 7: Add Shields/Badges

The README already includes badges for:
- Python version
- License
- Platform support

These will automatically display once the repo is public.

## Alternative: Using GitHub CLI

If you have GitHub CLI installed:

```bash
# Create repo and push in one go
gh repo create port-scanner --public --source=. --remote=origin --push

# Or for private repo
gh repo create port-scanner --private --source=. --remote=origin --push
```

## Troubleshooting

### Authentication Issues

If you can't push, you may need to:

1. Use personal access token instead of password
2. Set up SSH keys
3. Use GitHub CLI for authentication

### Already Initialized Error

If git is already initialized:

```bash
rm -rf .git
git init
# Then continue with Step 2
```

### Branch Name Issues

If your default branch isn't `main`:

```bash
git branch -M main
git push -u origin main
```

## Next Steps

After publishing:

1. Create a release (v1.0.0) on GitHub
2. Add screenshots or demo GIF to README
3. Write a blog post about the project
4. Share on social media
5. Monitor issues and pull requests
6. Continue development!

## Quick Commands Reference

```bash
# Clone your repo elsewhere
git clone https://github.com/YOUR-USERNAME/port-scanner.git

# Make changes and push
git add .
git commit -m "Your commit message"
git push

# Create new branch for feature
git checkout -b feature-name
git push -u origin feature-name

# Check status
git status

# View commit history
git log --oneline
```

## Portfolio Tips

To showcase this project in your portfolio:

1. Add a demo GIF or screenshots to README
2. Write clear, detailed README (already done!)
3. Show commit history with meaningful messages
4. Respond to issues/PRs professionally
5. Keep code well-commented
6. Add tests if possible
7. Document design decisions
8. Include performance benchmarks

Good luck with your portfolio!
