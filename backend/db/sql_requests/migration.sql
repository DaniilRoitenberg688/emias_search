ALTER TABLE mm.mdoc ADD COLUMN fio_tsv tsvector
  GENERATED ALWAYS AS (
    to_tsvector('russian', coalesce(surname,'') || ' ' || coalesce(name,'') || ' ' || coalesce(patron,''))
  ) STORED;

CREATE INDEX idx_pat_fio_tsv ON mm.mdoc USING gin (fio_tsv);