PRAGMA foreign_keys=off;

ALTER TABLE note RENAME TO note_orig;

CREATE TABLE note (
	id INTEGER NOT NULL,
	title VARCHAR NOT NULL,
	PRIMARY KEY (id),
	CONSTRAINT note_non_blank_title CHECK (length(trim(title, ' ')) > 0)
);

INSERT INTO note (id, title) SELECT id, title FROM note_orig;

DROP TABLE note_orig;

PRAGMA foreign_keys=on;
