# API shutdown.fyi

Базовый адрес: `https://shutdown.fyi`. Ответы — JSON в UTF-8, время — ISO 8601 по Москве (`+03:00`).
Ключ не нужен. Лицензия данных — CC BY 4.0, со ссылкой на shutdown.fyi.

## `GET /api/status.json`

Все сущности одним запросом. Кэш 60 секунд.

```json
{
  "generatedAt": "2026-09-21T17:09:00+03:00",
  "license": "CC BY 4.0 — shutdown.fyi",
  "country": { "status": "ok", "score": 0, "connectivityIndex": 100, "computedAt": "…" },
  "items": [
    {
      "entity": "service:telegram", "kind": "service", "slug": "telegram", "name": "Telegram",
      "status": "ok", "score": 0, "confidence": 1,
      "reports1h": 0, "reports24h": 2, "baseline1h": 0,
      "anomalyShare": 0.81, "iodaDrop": null,
      "changedAt": "…", "computedAt": "…", "url": "https://shutdown.fyi/telegram/"
    }
  ]
}
```

| Поле | Смысл |
|---|---|
| `status` | `ok`, `degraded` (сбои), `down` (массовый сбой), `unknown` (сигналов мало) — **изменение относительно нормы**, не факт блокировки |
| `score` | индекс 0…1, из которого выводится статус (пороги — в методике) |
| `confidence` | доля входов, по которым есть данные |
| `reports1h`, `reports24h` | жалобы с самого сайта (кнопка «не работает») |
| `baseline1h` | норма жалоб для этого часа |
| `anomalyShare` | доля аномальных измерений OONI за последние часы |
| `iodaDrop` | просадка трафика по IODA (для операторов и регионов) |
| `connectivityIndex` | индекс связности страны, 100 — всё открывается |

## `GET /api/status/{kind}/{slug}.json`

`kind` — `service`, `operator` или `region`. Всё из списка выше плюс:

- `external` — жалобы на внешних детекторах: `complaints1h`, `complaints24h`, `hourly24` и разбивка `sources[]` по источникам (Сбой.рф, DownRadar, ДомИнтернет, Outage.Report и др.);
- `probe` — активные проверки доступа (только у сервисов):

```json
{
  "verdict": "blocked",
  "checkedAt": "2026-09-21T17:08:00+03:00",
  "hosts": [{
    "host": "www.youtube.com",
    "verdict": "blocked-tls",
    "ru":     { "ip": "142.251.155.4", "pingMs": 20, "tcp": "ok", "tcpMs": 20, "tls": "timeout", "http": null },
    "abroad": { "tcp": "ok", "tls": "ok", "tlsMs": 7, "http": 200 }
  }]
}
```

`verdict`: `open`, `blocked` (из России не открывается, снаружи открывается), `partial`, `geo` (сервис сам отказывает российским адресам), `down` (не открывается ни оттуда, ни оттуда), `fail` (вывода нет), `none` (проверок нет).
Для хоста: `blocked-dns`, `blocked-tcp`, `blocked-tls` — на каком шаге обрывается соединение из России.

- `history24` — статус и индекс по часам за сутки;
- `openIncident` — текущий инцидент или `null`;
- `pattern` — сколько часов из недели были со сбоями, типичное окно суток, средняя длительность.

## `GET /api/incidents.json`

Инциденты за 7 дней.

```json
{ "generatedAt": "…", "count": 57, "incidents": [
  { "id": 56, "entity": "service:vk-video", "name": "VK Видео", "severity": "degraded",
    "title": "Сбой VK Видео", "startedAt": "…", "endedAt": null, "durationSec": 317,
    "url": "https://shutdown.fyi/vk-video/", "post": null }
]}
```

## Ограничения

- до 60 запросов в минуту с адреса;
- цифры пересчитываются раз в несколько минут;
- внешние детекторы — чужие данные, мы приводим их как есть и нормируем: у одних есть почасовой ряд, у других только «за сутки», и такие распределяются по часам равномерно.
