# ☦️ მართლმადიდებლური კალენდრის API / Orthodox Liturgical Calendar API

მრავალენოვანი (**ქართული • English • Русский**) მართლმადიდებლური საეკლესიო კალენდრის REST API და Python ბიბლიოთეკა.

შექმნილია იმისათვის, რომ ნებისმიერ აპლიკაციას (მობილური, ვებ-გვერდი, Telegram/Discord ბოტი) შეეძლოს კონკრეტული თარიღის მიხედვით მართლმადიდებლური დღესასწაულების, წმინდანთა ხსენების, ძველი/ახალი სტილის თარიღებისა და მარხვის წესების წამოღება.

---

## 🌟 ძირითადი ფუნქციები (Features)

- 🇬🇪 **ქართული მართლმადიდებლური ტრადიცია**: განსაკუთრებული აქცენტი ქართველ წმინდანებსა და დღესასწაულებზე (სვეტიცხოვლობა, გიორგობა, ნინოობა, დავით აღმაშენებელი, თამარ მეფე, 100,000 მოწამე, აბო თბილელი, ასურელი მამები და სხვ.).
- 🌐 **მრავალენოვნება (Multilingual)**: სრული მხარდაჭერა 3 ენაზე:
  - `ka` — ქართული (Georgian)
  - `en` — English
  - `ru` — Русский (Russian)
- 📅 **ძველი და ახალი სტილი (Julian & Revised Julian)**:
  - ძველი სტილი (`calendar=old`, ნაგულისხმევი) — საქართველოსა და სლავური ეკლესიების კალენდარი (+13 დღე გრიგორიანულთან).
  - ახალი სტილი (`calendar=new`) — შესწორებული იულიუსის კალენდარი.
- 🕊️ **მოძრავი ციკლი და აღდგომა (Paschal Cycle)**:
  - მართლმადიდებლური პასქალიის ზუსტი ასტრონომიული ალგორითმი (Meeus Julian Pascha).
  - დიდმარხვა, მეზვერე და ფარისეველი, ყველიერი, ლაზარეს შაბათი, ბზობა, ვნების კვირა, აღდგომა, ბრწყინვალე შვიდეული, ამაღლება, სულთმოფენობა (სამება), პეტრე-პავლობის მარხვა.
- 🍽️ **მარხვის წესების ავტომატური განსაზღვრა**:
  - ხსნილი, მკაცრი მარხვა (უზეთო), ზეთითა და ღვინით, თევზით ხსნილი, ყველიერი (რძის ნაწარმით), ხსნილი შვიდეულები.
- ⚡ **Zero Dependencies (0 დამოკიდებულება)**:
  - ძირითადი სერვერი მუშაობს სუფთა Python 3 სტანდარტული ბიბლიოთეკით, ყოველგვარი `pip install`-ის გარეშე.
  - პარალელურად მხარდაჭერილია **FastAPI** (`app.fastapi_app`) და **Docker**.
- 📖 **ინტერაქტიული დოკუმენტაცია**:
  - ჩაშენებული Swagger UI `/docs` მისამართზე.

---

## 🚀 სწრაფი გაშვება (Quickstart)

### ვარიანტი 1: სუფთა Python (Zero dependencies — არ საჭიროებს ინსტალაციას)

```bash
git clone https://github.com/your-username/orthodox-calendar-api.git
cd orthodox-calendar-api

# სერვერის გაშვება (ნაგულისხმევი პორტი: 8000)
python3 -m app.main
```
გახსენით ბრაუზერში:
- 🌐 მთავარი გვერდი: [http://localhost:8000](http://localhost:8000)
- 📖 Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- 📅 დღევანდელი დღე: [http://localhost:8000/api/v1/today](http://localhost:8000/api/v1/today)

---

### ვარიანტი 2: Docker / Docker Compose

```bash
docker compose up -d
```
სერვერი ხელმისაწვდომია მისამართზე: `http://localhost:8000`

---

### ვარიანტი 3: FastAPI & Uvicorn

```bash
pip install -r requirements.txt
uvicorn app.fastapi_app:app --host 0.0.0.0 --port 8000 --reload
```

---

## 💻 CLI (ტერმინალის ბრძანებები)

პროექტს მოყვება მოსახერხებელი CLI ინტერფეისი:

```bash
# დღევანდელი დღის ინფორმაცია ქართულად
python3 -m app.cli today --lang ka

# კონკრეტული თარიღის ინფორმაცია (მაგ: სვეტიცხოვლობა)
python3 -m app.cli 2026-10-14 --lang ka

# ინგლისურად ან რუსულად
python3 -m app.cli 2026-01-07 --lang en
python3 -m app.cli 2026-01-07 --lang ru

# აღდგომის თარიღი და მთელი მოძრავი ციკლი
python3 -m app.cli pascha 2026

# წლის უდიდესი დღესასწაულები
python3 -m app.cli feasts 2026
```

---

## 📡 REST API დოკუმენტაცია

### 1. დღევანდელი დღის ინფორმაცია
`GET /api/v1/today`

**პარამეტრები (Query Parameters):**
- `lang`: `ka` (ქართული, default), `en` (ინგლისური), `ru` (რუსული)
- `calendar`: `old` (ძველი სტილი, default), `new` (ახალი სტილი)

**მაგალითი:**
```bash
curl -s "http://localhost:8000/api/v1/today?lang=ka"
```

---

### 2. კონკრეტული თარიღის ინფორმაცია
`GET /api/v1/day?date=YYYY-MM-DD` ან `GET /api/v1/day/{year}/{month}/{day}`

**მაგალითი:**
```bash
curl -s "http://localhost:8000/api/v1/day?date=2026-10-14&lang=ka"
```

**JSON პასუხის ნიმუში (სვეტიცხოვლობა):**
```json
{
  "gregorian_date": "2026-10-14",
  "julian_date": "2026-10-01",
  "weekday": {
    "index": 2,
    "name": "ოთხშაბათი"
  },
  "calendar_style": "old",
  "language": "ka",
  "title": "სვეტიცხოვლობა — კვართისა საუფლოისა და სვეტისა ცხოველსმყოფელისა. საფარველი ყოვლადწმიდისა ღვთისმშობლისა (მცხეთობა)",
  "feasts": [
    {
      "code": "protection_svetitskhoveli",
      "level": "georgian_great"
    }
  ],
  "movable_feast": null,
  "saints": [
    "სვეტიცხოვლობა — უფლის უკერველი კვართისა და სვეტისა ცხოველსმყოფელისა და მირონმდინარისა დღესასწაული (საქართველოს ეროვნული დღესასწაული)",
    "საფარველი ყოვლადწმიდისა ღვთისმშობლისა (ვლაქერნის სასწაული)",
    "ღირსი რომანოზ უტკბილესმგალობელი"
  ],
  "fasting": {
    "is_fast": true,
    "type": "wine_oil",
    "name": "მარხვა (ზეთითა და ღვინით)",
    "description": "ნებადართულია მცენარეული ზეთი და ღვინო",
    "reason": "ოთხშაბათისა და პარასკევის მარხვა"
  }
}
```

---

### 3. მთლიანი თვის კალენდარი
`GET /api/v1/month/{year}/{month}`

**მაგალითი:**
```bash
curl -s "http://localhost:8000/api/v1/month/2026/10?lang=ka"
```

---

### 4. აღდგომა და მოძრავი ციკლი
`GET /api/v1/pascha/{year}`

**მაგალითი:**
```bash
curl -s "http://localhost:8000/api/v1/pascha/2026?lang=ka"
```

**JSON პასუხის ნიმუში:**
```json
{
  "year": 2026,
  "orthodox_pascha": {
    "gregorian_date": "2026-04-12",
    "julian_date": "2026-03-30"
  },
  "movable_cycle_events": [
    {
      "date": "2026-02-23",
      "offset": -48,
      "code": "clean_monday",
      "type": "fast_start",
      "title": "სუფთა ორშაბათი — დიდმარხვის დასაწყისი"
    },
    {
      "date": "2026-04-05",
      "offset": -7,
      "code": "palm_sunday",
      "type": "twelve_feast",
      "title": "ბზობა — უფლის დიდებით შესვლა იერუსალიმში"
    },
    {
      "date": "2026-04-12",
      "offset": 0,
      "code": "pascha",
      "type": "feast_of_feasts",
      "title": "ქრისტეს ბრწყინვალე აღდგომა (პასექი)"
    },
    {
      "date": "2026-05-21",
      "offset": 39,
      "code": "ascension",
      "type": "twelve_feast",
      "title": "ამაღლება უფლისა ჩვენისა იესო ქრისტესი"
    },
    {
      "date": "2026-05-31",
      "offset": 49,
      "code": "pentecost",
      "type": "twelve_feast",
      "title": "სულთმოფენობა (წმინდა სამების დღე)"
    }
  ]
}
```

---

### 5. წლის უდიდესი დღესასწაულები
`GET /api/v1/feasts/{year}`

**მაგალითი:**
```bash
curl -s "http://localhost:8000/api/v1/feasts/2026?lang=ka"
```

---

## 🛠️ ინტეგრაციის მაგალითები სხვა აპლიკაციებში

### JavaScript / TypeScript (Fetch API):
```javascript
async function getTodayCalendar(lang = 'ka') {
  const response = await fetch(`http://localhost:8000/api/v1/today?lang=${lang}`);
  const data = await response.json();
  console.log(`დღეს არის: ${data.title}`);
  console.log(`მარხვა: ${data.fasting.name}`);
  return data;
}

getTodayCalendar();
```

### Python (Requests / Urllib):
```python
import urllib.request
import json

url = "http://localhost:8000/api/v1/day?date=2026-10-14&lang=ka"
with urllib.request.urlopen(url) as response:
    calendar_day = json.loads(response.read().decode())
    print("დღესასწაული:", calendar_day["title"])
    print("წმინდანები:", calendar_day["saints"])
    print("მარხვა:", calendar_day["fasting"]["name"])
```

---

## 🧪 ტესტების გაშვება (Testing)

პროექტი შეიცავს 30-ზე მეტ ავტომატურ ტესტს:
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

---

## 📁 პროექტის სტრუქტურა

```
orthodox-calendar-api/
├── app/
│   ├── core/
│   │   ├── calendar_service.py # მთავარი სერვისი (დღე, თვე, დღესასწაულები)
│   │   ├── fasting.py          # მარხვის წესების ლოგიკა
│   │   └── pascha.py           # აღდგომისა და კალენდრის გამოთვლები
│   ├── data/
│   │   ├── movable_feasts.py   # მოძრავი დღესასწაულების სახელები 3 ენაზე
│   │   └── saints_all.json     # 366 დღის წმინდანთა ბაზა (ka, en, ru)
│   ├── server.py               # Zero-dependency HTTP REST API სერვერი
│   ├── fastapi_app.py          # FastAPI ალტერნატივა
│   ├── cli.py                  # ტერმინალის CLI ხელსაწყო
│   └── main.py                 # აპლიკაციის მთავარი entrypoint
├── tests/
│   ├── test_pascha.py          # აღდგომის გამოთვლების ტესტები
│   ├── test_fasting.py         # მარხვის წესების ტესტები
│   ├── test_calendar_service.py# კალენდრისა და ენების ტესტები
│   └── test_api.py             # REST API ენდფოინთების ტესტები
├── examples/
│   ├── curl_examples.sh        # cURL მაგალითების სკრიპტი
│   ├── fetch_example.js        # JavaScript მაგალითი
│   └── python_client.py        # Python კლიენტის მაგალითი
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions ავტომატური ტესტები
├── Dockerfile                  # Docker კონტეინერი
├── docker-compose.yml          # Docker Compose კონფიგურაცია
├── pyproject.toml              # პროექტის მეტამონაცემები
├── requirements.txt            # FastAPI დამატებითი დამოკიდებულებები
├── LICENSE                     # MIT ლიცენზია
└── README.md                   # დოკუმენტაცია
```

---

## 📄 ლიცენზია (License)

პროექტი ვრცელდება [MIT](LICENSE) ლიცენზიით. თავისუფალია ნებისმიერი კომერციული თუ არაკომერციული გამოყენებისთვის.
