### LNX Edge API Client
###### Written for Python ≥ 3.7

---

#### Behavioral rules of thumb:

When requesting a report:
  - Pass _date_ (YYYY-MM-DD) strings instead of _datetime_ strings (YYYY-MM-DDTHH:MM:SS.sss) to the `dateRange` field.
  - Timezone should _always_ be specified in the request body. `EdgeAPI._get_report(...)` defaults to 
  `America/New_York`, but can be overridden.

---

#### Test script:
```shell script
(venv) > python -i test.py
```

