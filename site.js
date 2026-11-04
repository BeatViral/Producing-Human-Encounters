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

for (const form of document.querySelectorAll('.responses form')) {
  if (!config.contactEmail) continue;
  form.action = 'https://formsubmit.co/' + config.contactEmail;
  form.querySelector('button').disabled = false;
}
