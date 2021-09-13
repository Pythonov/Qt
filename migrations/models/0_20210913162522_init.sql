-- upgrade --
CREATE TABLE IF NOT EXISTS "brandname" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(100)  UNIQUE
);
CREATE TABLE IF NOT EXISTS "category" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(100)  UNIQUE
);
CREATE TABLE IF NOT EXISTS "drug" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(100)  UNIQUE,
    "category_id" INT REFERENCES "category" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "drugclass" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(100)  UNIQUE
);
CREATE TABLE IF NOT EXISTS "therapeuticuse" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(100)  UNIQUE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "drugs_usage" (
    "drug_id" INT NOT NULL REFERENCES "drug" ("id") ON DELETE CASCADE,
    "therapeuticuse_id" INT NOT NULL REFERENCES "therapeuticuse" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "drugs_class" (
    "drug_id" INT NOT NULL REFERENCES "drug" ("id") ON DELETE CASCADE,
    "drugclass_id" INT NOT NULL REFERENCES "drugclass" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "drugs_brands" (
    "drug_id" INT NOT NULL REFERENCES "drug" ("id") ON DELETE CASCADE,
    "brandname_id" INT NOT NULL REFERENCES "brandname" ("id") ON DELETE CASCADE
);
