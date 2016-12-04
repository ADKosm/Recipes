BEGIN;
--
-- Create model AlternativeConsists
--
CREATE TABLE "rcps_alternativeconsists" ("id" serial NOT NULL PRIMARY KEY, "quantity" varchar(200) NOT NULL);
--
-- Create model Comment
--
CREATE TABLE "rcps_comment" ("id" serial NOT NULL PRIMARY KEY, "comment_text" text NOT NULL, "comment_date" timestamp with time zone NOT NULL, "comment_author_id" integer NOT NULL);
--
-- Create model Consist
--
CREATE TABLE "rcps_consist" ("id" serial NOT NULL PRIMARY KEY, "quantity" varchar(200) NOT NULL);
--
-- Create model Equipment
--
CREATE TABLE "rcps_equipment" ("id" serial NOT NULL PRIMARY KEY, "equipment_name" varchar(200) NOT NULL, "equipment_alternative_id" integer NOT NULL);
--
-- Create model EquipmentCategory
--
CREATE TABLE "rcps_equipmentcategory" ("id" serial NOT NULL PRIMARY KEY, "ecategory_name" varchar(200) NOT NULL);
--
-- Create model Grade
--
CREATE TABLE "rcps_grade" ("id" serial NOT NULL PRIMARY KEY, "grade_stars" integer NOT NULL, "grade_favorite" boolean NOT NULL);
--
-- Create model Ingredient
--
CREATE TABLE "rcps_ingredient" ("id" serial NOT NULL PRIMARY KEY, "ingredient_name" varchar(200) NOT NULL);
--
-- Create model IngredientAlternative
--
CREATE TABLE "rcps_ingredientalternative" ("id" serial NOT NULL PRIMARY KEY, "alternative_quality" integer NOT NULL);
--
-- Create model IngredientCategory
--
CREATE TABLE "rcps_ingredientcategory" ("id" serial NOT NULL PRIMARY KEY, "icategory_name" varchar(200) NOT NULL);
--
-- Create model Recipe
--
CREATE TABLE "rcps_recipe" ("id" serial NOT NULL PRIMARY KEY, "recipe_name" varchar(200) NOT NULL, "recipe_rating" double precision NOT NULL, "recipe_link" varchar(500) NOT NULL);
--
-- Create model Tag
--
CREATE TABLE "rcps_tag" ("id" serial NOT NULL PRIMARY KEY, "tag_name" varchar(200) NOT NULL);
CREATE TABLE "rcps_tag_tag_recipes" ("id" serial NOT NULL PRIMARY KEY, "tag_id" integer NOT NULL, "recipe_id" integer NOT NULL);
--
-- Add field alternative_recipe to ingredientalternative
--
ALTER TABLE "rcps_ingredientalternative" ADD COLUMN "alternative_recipe_id" integer NOT NULL;
ALTER TABLE "rcps_ingredientalternative" ALTER COLUMN "alternative_recipe_id" DROP DEFAULT;
--
-- Add field alternative to ingredient
--
--
-- Add field ingredient_alternative to ingredient
--
ALTER TABLE "rcps_ingredient" ADD COLUMN "ingredient_alternative_id" integer NOT NULL;
ALTER TABLE "rcps_ingredient" ALTER COLUMN "ingredient_alternative_id" DROP DEFAULT;
--
-- Add field ingredient_category to ingredient
--
ALTER TABLE "rcps_ingredient" ADD COLUMN "ingredient_category_id" integer NOT NULL;
ALTER TABLE "rcps_ingredient" ALTER COLUMN "ingredient_category_id" DROP DEFAULT;
--
-- Add field recipe to ingredient
--
--
-- Add field grade_recipe to grade
--
ALTER TABLE "rcps_grade" ADD COLUMN "grade_recipe_id" integer NOT NULL;
ALTER TABLE "rcps_grade" ALTER COLUMN "grade_recipe_id" DROP DEFAULT;
--
-- Add field grader to grade
--
ALTER TABLE "rcps_grade" ADD COLUMN "grader_id" integer NOT NULL;
ALTER TABLE "rcps_grade" ALTER COLUMN "grader_id" DROP DEFAULT;
--
-- Add field equipment_category to equipment
--
ALTER TABLE "rcps_equipment" ADD COLUMN "equipment_category_id" integer NOT NULL;
ALTER TABLE "rcps_equipment" ALTER COLUMN "equipment_category_id" DROP DEFAULT;
--
-- Add field equipment_recipes to equipment
--
CREATE TABLE "rcps_equipment_equipment_recipes" ("id" serial NOT NULL PRIMARY KEY, "equipment_id" integer NOT NULL, "recipe_id" integer NOT NULL);
--
-- Add field ingredient to consist
--
ALTER TABLE "rcps_consist" ADD COLUMN "ingredient_id" integer NOT NULL;
ALTER TABLE "rcps_consist" ALTER COLUMN "ingredient_id" DROP DEFAULT;
--
-- Add field recipe to consist
--
ALTER TABLE "rcps_consist" ADD COLUMN "recipe_id" integer NOT NULL;
ALTER TABLE "rcps_consist" ALTER COLUMN "recipe_id" DROP DEFAULT;
--
-- Add field comment_recipe to comment
--
ALTER TABLE "rcps_comment" ADD COLUMN "comment_recipe_id" integer NOT NULL;
ALTER TABLE "rcps_comment" ALTER COLUMN "comment_recipe_id" DROP DEFAULT;
--
-- Add field ingredient to alternativeconsists
--
ALTER TABLE "rcps_alternativeconsists" ADD COLUMN "ingredient_id" integer NOT NULL;
ALTER TABLE "rcps_alternativeconsists" ALTER COLUMN "ingredient_id" DROP DEFAULT;
--
-- Add field ingredient_alternative to alternativeconsists
--
ALTER TABLE "rcps_alternativeconsists" ADD COLUMN "ingredient_alternative_id" integer NOT NULL;
ALTER TABLE "rcps_alternativeconsists" ALTER COLUMN "ingredient_alternative_id" DROP DEFAULT;
ALTER TABLE "rcps_comment" ADD CONSTRAINT "rcps_comment_comment_author_id_9f0a190a_fk_auth_user_id" FOREIGN KEY ("comment_author_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcps_comment_73ad411d" ON "rcps_comment" ("comment_author_id");
ALTER TABLE "rcps_equipment" ADD CONSTRAINT "rcps_equ_equipment_alternative_id_ca88a171_fk_rcps_equipment_id" FOREIGN KEY ("equipment_alternative_id") REFERENCES "rcps_equipment" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcps_equipment_e9f13dfe" ON "rcps_equipment" ("equipment_alternative_id");
ALTER TABLE "rcps_tag_tag_recipes" ADD CONSTRAINT "rcps_tag_tag_recipes_tag_id_6274ddea_fk_rcps_tag_id" FOREIGN KEY ("tag_id") REFERENCES "rcps_tag" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "rcps_tag_tag_recipes" ADD CONSTRAINT "rcps_tag_tag_recipes_recipe_id_274b3a99_fk_rcps_recipe_id" FOREIGN KEY ("recipe_id") REFERENCES "rcps_recipe" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "rcps_tag_tag_recipes" ADD CONSTRAINT "rcps_tag_tag_recipes_tag_id_14f68454_uniq" UNIQUE ("tag_id", "recipe_id");
CREATE INDEX "rcps_tag_tag_recipes_76f094bc" ON "rcps_tag_tag_recipes" ("tag_id");
CREATE INDEX "rcps_tag_tag_recipes_da50e9c3" ON "rcps_tag_tag_recipes" ("recipe_id");
CREATE INDEX "rcps_ingredientalternative_ce7f09f4" ON "rcps_ingredientalternative" ("alternative_recipe_id");
ALTER TABLE "rcps_ingredientalternative" ADD CONSTRAINT "rcps_ingredien_alternative_recipe_id_1e19835e_fk_rcps_recipe_id" FOREIGN KEY ("alternative_recipe_id") REFERENCES "rcps_recipe" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcps_ingredient_9034f112" ON "rcps_ingredient" ("ingredient_alternative_id");
ALTER TABLE "rcps_ingredient" ADD CONSTRAINT "D3b54bf71f99ae3ce72bd8c2380c7521" FOREIGN KEY ("ingredient_alternative_id") REFERENCES "rcps_ingredientalternative" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcps_ingredient_35e87b50" ON "rcps_ingredient" ("ingredient_category_id");
ALTER TABLE "rcps_ingredient" ADD CONSTRAINT "r_ingredient_category_id_11f11ad7_fk_rcps_ingredientcategory_id" FOREIGN KEY ("ingredient_category_id") REFERENCES "rcps_ingredientcategory" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcps_grade_506c9557" ON "rcps_grade" ("grade_recipe_id");
ALTER TABLE "rcps_grade" ADD CONSTRAINT "rcps_grade_grade_recipe_id_6864347f_fk_rcps_recipe_id" FOREIGN KEY ("grade_recipe_id") REFERENCES "rcps_recipe" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcps_grade_768334c3" ON "rcps_grade" ("grader_id");
ALTER TABLE "rcps_grade" ADD CONSTRAINT "rcps_grade_grader_id_50f5a570_fk_auth_user_id" FOREIGN KEY ("grader_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcps_equipment_26e95bb3" ON "rcps_equipment" ("equipment_category_id");
ALTER TABLE "rcps_equipment" ADD CONSTRAINT "rcp_equipment_category_id_a83aa60a_fk_rcps_equipmentcategory_id" FOREIGN KEY ("equipment_category_id") REFERENCES "rcps_equipmentcategory" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "rcps_equipment_equipment_recipes" ADD CONSTRAINT "rcps_equipment_equip_equipment_id_cf11f877_fk_rcps_equipment_id" FOREIGN KEY ("equipment_id") REFERENCES "rcps_equipment" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "rcps_equipment_equipment_recipes" ADD CONSTRAINT "rcps_equipment_equipment_r_recipe_id_86484d6a_fk_rcps_recipe_id" FOREIGN KEY ("recipe_id") REFERENCES "rcps_recipe" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "rcps_equipment_equipment_recipes" ADD CONSTRAINT "rcps_equipment_equipment_recipes_equipment_id_36db8415_uniq" UNIQUE ("equipment_id", "recipe_id");
CREATE INDEX "rcps_equipment_equipment_recipes_997b9956" ON "rcps_equipment_equipment_recipes" ("equipment_id");
CREATE INDEX "rcps_equipment_equipment_recipes_da50e9c3" ON "rcps_equipment_equipment_recipes" ("recipe_id");
CREATE INDEX "rcps_consist_7a06a9e2" ON "rcps_consist" ("ingredient_id");
ALTER TABLE "rcps_consist" ADD CONSTRAINT "rcps_consist_ingredient_id_4fbd8fc3_fk_rcps_ingredient_id" FOREIGN KEY ("ingredient_id") REFERENCES "rcps_ingredient" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcps_consist_da50e9c3" ON "rcps_consist" ("recipe_id");
ALTER TABLE "rcps_consist" ADD CONSTRAINT "rcps_consist_recipe_id_a167f5ff_fk_rcps_recipe_id" FOREIGN KEY ("recipe_id") REFERENCES "rcps_recipe" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcps_comment_8fbbe8a6" ON "rcps_comment" ("comment_recipe_id");
ALTER TABLE "rcps_comment" ADD CONSTRAINT "rcps_comment_comment_recipe_id_faa8ad80_fk_rcps_recipe_id" FOREIGN KEY ("comment_recipe_id") REFERENCES "rcps_recipe" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcps_alternativeconsists_7a06a9e2" ON "rcps_alternativeconsists" ("ingredient_id");
ALTER TABLE "rcps_alternativeconsists" ADD CONSTRAINT "rcps_alternativeco_ingredient_id_fb70b706_fk_rcps_ingredient_id" FOREIGN KEY ("ingredient_id") REFERENCES "rcps_ingredient" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "rcps_alternativeconsists_9034f112" ON "rcps_alternativeconsists" ("ingredient_alternative_id");
ALTER TABLE "rcps_alternativeconsists" ADD CONSTRAINT "ed5a97e4d1b7def6bfe62002fc1376ea" FOREIGN KEY ("ingredient_alternative_id") REFERENCES "rcps_ingredientalternative" ("id") DEFERRABLE INITIALLY DEFERRED;
COMMIT;
