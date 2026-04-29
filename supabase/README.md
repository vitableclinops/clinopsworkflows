# Supabase — provider data + activation candidate ranking

This directory holds the schema and seed tooling for the ClinOps provider
operational store. It replaces the Lovable / ClinOps Hub setup so we can run
on a Supabase project that has a BAA.

Project: `https://bbquooftytwprllipcsb.supabase.co`

## Layout

```
supabase/
├── migrations/                     # Apply in numeric order.
│   ├── 0001_create_providers.sql
│   ├── 0002_create_provider_licenses.sql
│   ├── 0003_create_provider_utilization_daily.sql
│   ├── 0004_get_activation_candidates.sql
│   └── 0005_enable_rls.sql
└── seed/
    ├── seed_providers.py           # Idempotent CSV → REST upsert.
    ├── providers.csv.example
    └── licenses.csv.example
```

## Apply migrations

**Option A — Supabase Studio (easiest, one-time):** Project → SQL Editor →
paste each file in order, run.

**Option B — Supabase CLI:** rename each file to a 14-digit timestamp prefix
(e.g. `20260429100001_create_providers.sql`) and run `supabase db push`.

**Option C — `psql`:**

```bash
PGPASSWORD=$DB_PASSWORD psql \
  "host=db.bbquooftytwprllipcsb.supabase.co user=postgres dbname=postgres sslmode=require" \
  -f migrations/0001_create_providers.sql \
  -f migrations/0002_create_provider_licenses.sql \
  -f migrations/0003_create_provider_utilization_daily.sql \
  -f migrations/0004_get_activation_candidates.sql \
  -f migrations/0005_enable_rls.sql
```

## Seed providers + licenses

1. Copy the example CSVs and fill them with real data:

   ```bash
   cp supabase/seed/providers.csv.example supabase/seed/providers.csv
   cp supabase/seed/licenses.csv.example  supabase/seed/licenses.csv
   ```

   The `.gitignore` keeps real rosters out of the repo.

2. Run the seed script with the **service-role** key (Studio → Project Settings
   → API → `service_role`, *not* the anon key):

   ```bash
   export SUPABASE_URL=https://bbquooftytwprllipcsb.supabase.co
   export SUPABASE_SERVICE_ROLE_KEY=eyJ...
   python supabase/seed/seed_providers.py \
     --providers supabase/seed/providers.csv \
     --licenses  supabase/seed/licenses.csv
   ```

   Re-running is safe: providers upsert on `email`, licenses on
   `(provider_id, state)`.

## RPC: get_activation_candidates

Replaces the Lovable `suggest-activation-candidates` edge function.

```sql
select * from get_activation_candidates(
  deficit_states    := array['PA','NJ'],
  util_threshold    := 70,
  candidate_limit   := 5,
  shift_type_filter := array['NP Telemedicine','MD Telemedicine']
);
```

REST/curl form:

```bash
curl -s -X POST "$SUPABASE_URL/rest/v1/rpc/get_activation_candidates" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "deficit_states": ["PA","NJ"],
    "util_threshold": 70,
    "candidate_limit": 5,
    "shift_type_filter": ["NP Telemedicine","MD Telemedicine"]
  }'
```

Ranking within each state:

1. Lowest current utilization (NULL → treated as 0, i.e. highest priority)
2. `readiness_status` — `ready` before `training` before `paused`
3. Provider name (alphabetical, for stable ordering)

## Provider utilization sync

Not implemented yet — `provider_utilization_daily` is empty until we wire a
sync from Metabase's Daily Provider Utilization card. Until then,
`get_activation_candidates` ranks every candidate as if utilization were 0,
which is fine for bootstrap.

## RLS

All three tables are RLS-enabled with deny-by-default for `anon` and
`authenticated`. The service-role key bypasses RLS, which is what the daily
report job uses. No frontend access until we add explicit policies.
