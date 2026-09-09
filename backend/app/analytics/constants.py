"""
Analytics calculation constants.

These are documented estimates used for derived metrics. Any change to these
values requires:
  1. A PR against contracts/openapi-frozen.json
  2. Sign-off from the analytics consumer (admin dashboard owner = Person 6)
  3. A changelog entry in contracts/CHANGELOG.md

Sources:
  - MEAL_WEIGHT_KG: 0.5 kg/meal — common food-rescue-sector working estimate
    (used by, e.g., Feeding America's methodology).
  - MEALS_PER_BENEFICIARY_PER_PERIOD: 14 — estimate of meals consumed by one
    beneficiary over a 7-day reference period (2 meals/day × 7 days).
    This constant is used only when real beneficiary tracking data is absent;
    the beneficiaries_reached field is explicitly annotated as an estimate
    in the API response.
"""

# kg of food that constitutes one meal (working estimate, not a measured figure)
MEAL_WEIGHT_KG: float = 0.5

# meals attributable to one beneficiary over the reference period (7 days)
MEALS_PER_BENEFICIARY_PER_PERIOD: int = 14

# Shelf-life score threshold below which a donation is considered high-risk.
# Donations with shelf_life_score < this value at match time are counted in
# the "spoilage_risk_avoided" metric if they are ultimately delivered.
SPOILAGE_RISK_THRESHOLD: float = 0.3
