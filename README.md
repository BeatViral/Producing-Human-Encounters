# Producing Human Encounters

Static national website and eight city-series pages for GitHub Pages.

## Edit and preview

1. Edit copy and city entries in `build_site.py`. Set the shared enquiry address in `site-config.json`.
2. Run `python build_site.py` to regenerate the homepage, eight city pages and sitemap.
3. Run `python -m http.server 8000` from the repository root and open http://localhost:8000.
4. When ready to publish, commit the source and generated files and push to `main`. GitHub Pages serves `main` from the repository root.

The three enquiry links open addressed drafts with city-specific subjects. The visitor reviews and sends the draft from their email app.

## Replace artwork

Keep the supplied PNG originals in `assets/posters/` under their existing names. Update each matching full-size WebP (up to 900 px wide), city tile WebP (450 px wide), and 1200 × 630 JPEG share card. Update the national hero portrait crops in `assets/national-left.webp` and `assets/national-right.webp`, and the gathering crop in `assets/national-gathering.webp` when replacing the national poster. Keep the posters intact in the full WebP and downloadable PNG. Use landscape or gathering details for share crops and keep QR graphics out of those crops.

## Connect the permanent domain when ready

1. After securing `producinghumanencounters.com`, verify it in the BeatViral account’s **Settings → Pages** using the DNS TXT record GitHub supplies.
2. In this repository’s **Settings → Pages → Custom domain**, enter `producinghumanencounters.com` and save.
3. At the DNS provider, point the apex (`@`) to GitHub Pages with four A records: `185.199.108.153`, `185.199.109.153`, `185.199.110.153` and `185.199.111.153`. For `www`, add a CNAME to `beatviral.github.io`. Keep the verification TXT record.
4. Wait for the Pages DNS and certificate checks. Enable **Enforce HTTPS** when available and check the homepage and city URLs over HTTPS.
5. Change `siteUrl` in `site-config.json` to `https://producinghumanencounters.com/`, run `python build_site.py`, and publish the generated canonical URLs, social metadata and sitemap. Verify the poster QR codes open the live homepage before distributing them.

See [GitHub’s custom domain documentation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site) for DNS verification and troubleshooting.
