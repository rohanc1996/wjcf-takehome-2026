import csv
import random
from pathlib import Path

from faker import Faker

SEED = 42
OUT = Path(__file__).resolve().parent / "data"
OUT.mkdir(parents=True, exist_ok=True)

random.seed(SEED)
Faker.seed(SEED)
fake = Faker("en_IN")

N_DISTRICTS = 20
DIST_PER_STATE = 5
N_STATES = 4

ELIGIBLE_MIN = 350
ELIGIBLE_MAX = 700

SPECIALTIES = ["General Medicine", "Cardiology", "Orthopaedics", "Paediatrics",
               "Obstetrics", "Oncology", "Ophthalmology", "General Surgery",
               "Nephrology", "Neurology"]
PACKAGES = [f"PKG{i:03d}" for i in range(1, 61)]
PACKAGE_NAMES = ["Hernia Repair", "Cataract Surgery", "Coronary Bypass", "Knee Replacement",
                 "Pneumonia Care", "Dengue Care", "C-section Delivery", "Kidney Stone Removal",
                 "Appendectomy", "Stroke Care", "Dialysis Session", "Hip Replacement",
                 "Diabetes Care", "Typhoid Care", "Hysterectomy"]

STATES = ["State_1", "State_2", "State_3", "State_4"]


def district_state(d_id):
    state = (d_id - 1) // DIST_PER_STATE + 1
    return d_id, state


# eligible population reference (denominator for coverage)
eligible_pop = {}
for d in range(1, N_DISTRICTS + 1):
    eligible_pop[d] = random.randint(ELIGIBLE_MIN, ELIGIBLE_MAX)

# districts 7 and 13 engineered to show coverage above 100%, for different reasons:
# 7 = duplicate / fraudulent beneficiary entries push the row count over eligible population
# 13 = eligible_population is understated (stale 2011 census, state-funded top-up expands eligibility)
eligible_pop[7] = 280
eligible_pop[13] = 230

with (OUT / "eligible_population.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["district_id", "eligible_population"])
    for d in range(1, N_DISTRICTS + 1):
        w.writerow([d, eligible_pop[d]])

# beneficiaries: card holders per district
beneficiaries = []
beneficiary_id = 1
card_holders = {}
district_dup_rows = {}
for d in range(1, N_DISTRICTS + 1):
    if d == 7:
        n = int(eligible_pop[d] * 0.85)
        dup_rows = int(n * 0.24)
    elif d == 13:
        n = int(eligible_pop[d] * 1.35)
        dup_rows = 0
    else:
        n = int(eligible_pop[d] * random.uniform(0.35, 0.95))
        dup_rows = 0
    card_holders[d] = n
    district_dup_rows[d] = dup_rows
    for _ in range(n):
        fam = beneficiary_id // 3 + 1
        age = random.choices(range(0, 101), weights=[2] * 20 + [1] * 81)[0]
        gender = random.choice(["M", "F"])
        beneficiaries.append([beneficiary_id, fam, d, district_state(d)[1], age, gender])
        beneficiary_id += 1
    for _ in range(dup_rows):
        row = random.choice(beneficiaries[-n:])
        beneficiaries.append(list(row))

with (OUT / "beneficiaries.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["beneficiary_id", "family_id", "district_id", "state_id", "age", "gender"])
    w.writerows(beneficiaries)

# facilities
facilities = []
hospital_id = 1
for d in range(1, N_DISTRICTS + 1):
    n = random.randint(6, 14)
    if d in (3, 11, 17):
        n = 4  # low-supply districts
    private_prob = random.uniform(0.2, 0.8)
    base_lat = 21.0 + d * 0.2
    base_lon = 78.0 + (d % 5) * 0.3
    for _ in range(n):
        ftype = "private" if random.random() < private_prob else "public"
        emp = "de-empanelled" if random.random() < 0.15 else "empanelled"
        act = "dormant" if random.random() < 0.12 else "active"
        if d in (3, 11, 17) and random.random() < 0.5:
            emp = "de-empanelled"
            act = "dormant"
        bed = random.randint(50, 500) if ftype == "public" else random.randint(20, 200)
        lat = round(base_lat + random.uniform(-0.05, 0.05), 4)
        lon = round(base_lon + random.uniform(-0.05, 0.05), 4)
        facilities.append([hospital_id, fake.company() + " Hospital", d, district_state(d)[1],
                           ftype, emp, act, bed, lat, lon])
        hospital_id += 1

with (OUT / "facilities.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["hospital_id", "hospital_name", "district_id", "state_id", "facility_type",
                 "empanelment_status", "activity_status", "bed_count", "lat", "lon"])
    w.writerows(facilities)

# claims
claims = []
claim_id = 1
date_start = __import__("datetime").date(2024, 1, 1)
date_end = __import__("datetime").date(2025, 6, 30)


def rand_date():
    return fake.date_between(start_date=date_start, end_date=date_end)


for d in range(1, N_DISTRICTS + 1):
    facs = [f for f in facilities if f[2] == d]
    good = [f for f in facs if f[5] == "empanelled" and f[6] == "active"]
    bad = [f for f in facs if f[5] == "de-empanelled" or f[6] == "dormant"]
    active = [f for f in facs if f[6] == "active" and f[5] == "empanelled"]
    private_share = (sum(1 for f in active if f[4] == "private") / len(active)) if active else 0.5
    claims_per_card = 3.0 - 2.0 * private_share
    n_claims = max(150, int(card_holders[d] * claims_per_card * random.uniform(0.9, 1.1)))
    district_bens = [b for b in beneficiaries if b[2] == d]
    for _ in range(n_claims):
        b = random.choice(district_bens)
        hosp = random.choice(good) if good else random.choice(facs)
        pkg = random.choice(PACKAGES)
        claim_amount = random.randint(3000, 150000)
        status = random.choices(["approved", "rejected", "pending"], weights=[55, 23, 22])[0]
        if status == "approved":
            approved_amount = int(claim_amount * random.uniform(0.4, 1.0))
        elif status == "pending":
            approved_amount = int(claim_amount * random.uniform(0.0, 0.6))
        else:
            approved_amount = 0
        admitted = rand_date()
        discharged = admitted + __import__("datetime").timedelta(days=random.randint(1, 15))
        claims.append([claim_id, b[0], b[1], d, district_state(d)[1], hosp[0], pkg,
                       random.choice(PACKAGE_NAMES), random.choice(SPECIALTIES),
                       claim_amount, approved_amount, admitted, discharged, status,
                       b[4], b[5]])
        claim_id += 1

# planted dirt
n_dupes = 60
dupes = [list(c) for c in random.sample(claims, n_dupes)]
claims.extend(dupes)

bad_hospitals = [f[0] for f in facilities if f[5] == "de-empanelled" or f[6] == "dormant"]
for c in random.sample(claims, 80):
    c[5] = random.choice(bad_hospitals)

for c in random.sample(claims, 30):
    c[12] = c[11] - __import__("datetime").timedelta(days=random.randint(1, 10))

for c in random.sample(claims, 40):
    c[10] = c[9] + random.randint(1, 100000)

for c in random.sample(claims, 20):
    c[9] = -abs(c[9])

for c in random.sample(claims, 25):
    c[14] = random.randint(120, 160)

for c in random.sample(claims, 25):
    c[3] = None

for c in random.sample(claims, 25):
    c[6] = None

for c in random.sample(claims, 20):
    c[11] = None

for c in random.sample(claims, 10):
    c[12] = None

with (OUT / "claims.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["claim_id", "beneficiary_id", "family_id", "district_id", "state_id",
                 "hospital_id", "package_code", "package_name", "specialty",
                 "claim_amount", "approved_amount", "date_admitted", "date_discharged",
                 "claim_status", "beneficiary_age", "beneficiary_gender"])
    w.writerows(claims)

print(f"eligible_population.csv rows: {N_DISTRICTS}")
print(f"beneficiaries.csv rows: {len(beneficiaries)} (unique beneficiary_id: {len(set(b[0] for b in beneficiaries))})")
print(f"facilities.csv rows: {len(facilities)}")
print(f"claims.csv rows: {len(claims)} (unique claim_id: {len(set(c[0] for c in claims))})")
from collections import Counter
print("claim status distribution:", dict(Counter(c[13] for c in claims)))
for d in (7, 13):
    rows = [b for b in beneficiaries if b[2] == d]
    unique = len(set(b[0] for b in rows))
    print(f"coverage district {d}: {len(rows)} rows/{eligible_pop[d]} = {len(rows)/eligible_pop[d]:.2%} (unique ids {unique})")
