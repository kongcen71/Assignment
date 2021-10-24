BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER NOT NULL,
	"username"	VARCHAR(15),
	"email"	VARCHAR(50),
	"password"	VARCHAR(80),
	PRIMARY KEY("id"),
	UNIQUE("username"),
	UNIQUE("email")
);
INSERT INTO "user" VALUES (1,'arpanneupane','arpanneupane19@gmail.com','$2b$12$iMVGjiuC3mjhRRKEkKvAeedPqnNvPgJh6CoMHmC1FS.AHWnWOw2d6');
INSERT INTO "user" VALUES (2,'arpanneupane2','arpanneupane192@gmail.com','$2b$12$/ykmxp/9LVo0F.A27c2l4eYzmZnfeVzOdJPJPW0JTY0CZ4V0bPPf2');
INSERT INTO "user" VALUES (3,'bernard','bernard@cuhk.edu.hk','$2b$12$y1zjaDJhsODpnm8Iw//bW.uNYa.yS3gOZU7QEVR5xLu89YsRAOPAO');
INSERT INTO "user" VALUES (4,'kongcen','kongcen71@163.com','$2b$12$eHHW2SpZWYOWkfLkuNtAP.u/XT6iY.nUKT7YRvMqoxxOrfVxbTiEG');
COMMIT;
