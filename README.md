# Producing Human Encounters

Static website for the inaugural Mullumbimby Series.

## Preview

Run `python -m http.server 8000` from the repository root and open http://localhost:8000.

## Publish on GitHub Pages

1. Push to the repository’s `main` branch.
2. Under **Settings → Pages**, choose **Deploy from a branch**, then **main** and **/ (root)**.
3. After deployment, open the URL shown in Pages settings. If you use a different domain or repository name, update the Open Graph image URL in `index.html`.

## Update the series

Edit `config.js` for event information, the participation target and contact, social and ticket links. Set `contactEmail` to the approved public inbox to enable email drafts for introductions and nominations. With no inbox configured, visitors can download a personal copy of their form. This static site stores no submissions.

Portraits and the landscape scene were cropped from the supplied approved poster. When the public URL is confirmed, generate the QR code and save it as `assets/series-qr.svg`. Reserve a clear, light area on the print poster for the code and its quiet zone, and scan a print proof before distribution.
