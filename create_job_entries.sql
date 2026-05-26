CREATE TABLE IF NOT EXISTS job_entries (
    file_name TEXT NOT NULL,
    file_modified_at TIMESTAMP NOT NULL,
    job TEXT,
    do_val TEXT,

    blk TEXT,
    blk_scan TIMESTAMP,
    blk_do TEXT,

    gen TEXT,
    gen_scan TIMESTAMP,
    gen_do TEXT,

    pol TEXT,
    pol_scan TIMESTAMP,
    pol_do TEXT,

    eng TEXT,
    eng_scan TIMESTAMP,
    eng_do TEXT,

    dba TEXT,
    dba_scan TIMESTAMP,
    dba_do TEXT,

    inserted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT job_entries_pk PRIMARY KEY (file_name, file_modified_at)
);

CREATE INDEX IF NOT EXISTS idx_job_entries_job
    ON job_entries (job);

CREATE INDEX IF NOT EXISTS idx_job_entries_blk_scan
    ON job_entries (blk_scan);

CREATE INDEX IF NOT EXISTS idx_job_entries_gen_scan
    ON job_entries (gen_scan);

CREATE INDEX IF NOT EXISTS idx_job_entries_pol_scan
    ON job_entries (pol_scan);

CREATE INDEX IF NOT EXISTS idx_job_entries_eng_scan
    ON job_entries (eng_scan);

CREATE INDEX IF NOT EXISTS idx_job_entries_dba_scan
    ON job_entries (dba_scan);
