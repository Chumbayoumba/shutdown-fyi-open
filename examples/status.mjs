// Сервисы со сбоем прямо сейчас. Node 18+: node examples/status.mjs
// Данные: shutdown.fyi, CC BY 4.0.
const res = await fetch('https://shutdown.fyi/api/status.json');
const { country, items } = await res.json();
console.log(`Индекс связности: ${country.connectivityIndex}`);
const bad = items.filter((i) => i.status === 'degraded' || i.status === 'down');
if (!bad.length) console.log('Массовых сбоев сейчас нет.');
for (const i of bad) console.log(`${i.name}: ${i.status} — ${i.url}`);
