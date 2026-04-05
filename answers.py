connection = "sqlite:///clinical_trials.db"
task_1_sql = """
SELECT
    AVG(CASE WHEN m.drug != 'Плацебо' THEN m.condition_score END) - 
    AVG(CASE WHEN m.drug = 'Плацебо' THEN m.condition_score END) AS diff
FROM measurements m
JOIN trials t ON m.trial_id = t.trial_id
GROUP BY m.trial_id, t.start_date
ORDER BY t.start_date
"""
task_2_sql = """
WITH placebo_first AS (
    SELECT trial_id, condition_score
    FROM (
        SELECT
            trial_id,
            condition_score,
            ROW_NUMBER() OVER (PARTITION BY trial_id ORDER BY measurement_date ASC) AS rn
        FROM measurements
        WHERE drug = 'Плацебо'
    )
    WHERE rn = 1
),
placebo_last AS (
    SELECT trial_id, condition_score
    FROM (
        SELECT
            trial_id,
            condition_score,
            ROW_NUMBER() OVER (PARTITION BY trial_id ORDER BY measurement_date DESC) AS rn
        FROM measurements
        WHERE drug = 'Плацебо'
    )
    WHERE rn = 1
),
active_first AS (
    SELECT trial_id, condition_score
    FROM (
        SELECT
            trial_id,
            condition_score,
            ROW_NUMBER() OVER (PARTITION BY trial_id ORDER BY measurement_date ASC) AS rn
        FROM measurements
        WHERE drug != 'Плацебо'
    )
    WHERE rn = 1
),
active_last AS (
    SELECT trial_id, condition_score
    FROM (
        SELECT
            trial_id,
            condition_score,
            ROW_NUMBER() OVER (PARTITION BY trial_id ORDER BY measurement_date DESC) AS rn
        FROM measurements
        WHERE drug != 'Плацебо'
    )
    WHERE rn = 1
)
SELECT
    (al.condition_score - af.condition_score) -
    (pl.condition_score - pf.condition_score) AS diff
FROM trials t
JOIN placebo_first pf ON t.trial_id = pf.trial_id
JOIN placebo_last pl ON t.trial_id = pl.trial_id
JOIN active_first af ON t.trial_id = af.trial_id
JOIN active_last al ON t.trial_id = al.trial_id
ORDER BY t.trial_id
"""

