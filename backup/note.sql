BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "note" (
	"id"	INTEGER NOT NULL,
	"title"	VARCHAR(25),
	"note_body"	VARCHAR(100),
	"note_writer"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("note_writer") REFERENCES "user"("id")
);
INSERT INTO "note" VALUES (3,'new note by other user','new note by other user',2);
INSERT INTO "note" VALUES (4,'Prepare for class','Powerpoint and sample codes',3);
INSERT INTO "note" VALUES (5,'Forum Discussion','Respond to questions.',3);
COMMIT;
