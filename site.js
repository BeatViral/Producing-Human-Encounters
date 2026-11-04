import config from './config.js';

document.querySelector('#guest-range').textContent = config.guestRange;
document.querySelector('#guest-target').textContent = config.guestTarget;

for (const { title, status } of config.events) {
  const row = document.createElement('li');
  const name = document.createElement('h3');
  const timing = document.createElement('span');
  name.textContent = title;
  timing.textContent = status;
  row.append(name, timing);
  document.querySelector('#events').append(row);
}

for (const [label, url, placeholder] of [
  ['Contact', config.contactEmail && 'mailto:' + config.contactEmail, 'Contact details coming soon'],
  ['Social', config.socialUrl, 'Social links coming soon'],
  ['Tickets', config.ticketsUrl, 'Ticket information coming soon'],
]) {
  const item = document.createElement(url ? 'a' : 'span');
  if (url) item.href = url;
  item.textContent = url ? label : placeholder;
  document.querySelector('#footer-links').append(item);
}

for (const panel of document.querySelectorAll('.responses details')) {
  const form = panel.querySelector('form');
  const button = form.querySelector('button');
  const status = form.querySelector('.status');
  form.querySelector('.form-note').textContent = config.contactEmail
    ? 'This opens a draft in your email app. You can review it before sending.'
    : 'Submissions will open when contact details are available. You can download a copy for yourself in the meantime.';
  if (config.contactEmail) button.textContent = 'Open email draft';

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const subject = panel.dataset.kind === 'nominate' ? 'Nomination' : 'Expression of interest';
    const body = [
      'Producing Human Encounters | ' + subject,
      '',
      'Name: ' + data.get('name'),
      'Email: ' + data.get('email'),
      'Location: ' + data.get('location'),
      '',
      data.get('message'),
      '',
      'I agree to be contacted.',
    ].join('\r\n');
    if (config.contactEmail) {
      window.location.href = 'mailto:' + config.contactEmail
        + '?subject=' + encodeURIComponent(subject + ' | Producing Human Encounters')
        + '&body=' + encodeURIComponent(body);
      status.textContent = 'Send the draft from your email app to complete your submission.';
      return;
    }
    const url = URL.createObjectURL(new Blob([body], { type: 'text/plain;charset=utf-8' }));
    const download = document.createElement('a');
    download.href = url;
    download.download = panel.dataset.kind + '-producing-human-encounters.txt';
    download.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    status.textContent = 'Your copy was prepared for download. Nothing was submitted.';
  });
}
