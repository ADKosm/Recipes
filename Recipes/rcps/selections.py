from rcps.models import Recipe

_find_recipe_query_fmt = '''
with allowed_equipment as (                          -- сюда нужно вставить 'not', если инструменты запрещены
  select distinct id from rcps_equipment where equipment_name {is_equipment_allowed} in {equipment_tuple} -- здесь должны быть разрешенные инструменты
), replaceable_equipment as (
  select distinct eq.id
  from
    rcps_equipment eq
    join rcps_equipment_alternatives mtm on eq.id = mtm.from_equipment_id
    join rcps_equipment alt on mtm.to_equipment_id = alt.id
  where
    eq.id not in (select * from allowed_equipment) and alt.id in (select * from allowed_equipment)
), forbidden_by_equipment_recipes as (
  select distinct r.id
  from
    rcps_recipe r
    join rcps_requires on r.id = rcps_requires.recipe_id
    join rcps_equipment e on rcps_requires.equipment_id = e.id
  where e.id not in (select * from allowed_equipment) and e.id not in (select * from replaceable_equipment)
), allowed_ingredients as (
  select id from rcps_ingredient where ingredient_name in {allowed_ingredients} -- здесь должны быть разрешенные ингредиенты
), forbidden_ingredient_alternatives as (
  select distinct alt.id
  from
    rcps_ingredientalternative alt
    join rcps_alternativeconsists mtm on alt.id = mtm.ingredient_alternative_id
    join rcps_ingredient ing on mtm.ingredient_id = ing.id
  where
    ing.id not in (select * from allowed_ingredients)
), replaceable_ingredient_in_recipe as (
  select distinct con.recipe_id, ing.id
  from
    rcps_ingredient ing
    join rcps_consist con on ing.id = con.ingredient_id
    join rcps_ingredientreplacement rep on con.id = rep.ingredient_entry_id
  where
    ing.id not in (select * from allowed_ingredients) and rep.alternative_id not in (select * from forbidden_ingredient_alternatives)
), forbidden_by_ingredient_recipes as (
  select r.id
  from
    rcps_recipe r
    join rcps_consist con on r.id = con.recipe_id
  where
    con.ingredient_id not in (select * from allowed_ingredients) and (r.id, con.ingredient_id) not in (select * from replaceable_ingredient_in_recipe)
) select * from rcps_recipe where id not in (select * from forbidden_by_equipment_recipes) and id not in (select * from forbidden_by_ingredient_recipes)
'''


def find_recipes(allowed_ingredients: tuple, equipment: tuple, equipment_is_allowed: bool):
    entrance_modifier = '' if equipment_is_allowed else 'not'
    allowed_ingredients = "('{}')".format("', '".join(allowed_ingredients))
    equipment = "('{}')".format("', '".join(equipment))
    query = _find_recipe_query_fmt.format(is_equipment_allowed=entrance_modifier,
                                          equipment_tuple=equipment,
                                          allowed_ingredients=allowed_ingredients)
    print(query)
    return Recipe.objects.raw(query)


_most_commented_recipes_query = '''
WITH recipe_comments as (
    SELECT DISTINCT
      r.id id,
      count(1) comment_num
    FROM
      rcps_recipe r
      JOIN rcps_comment c ON r.id = c.comment_recipe_id
    GROUP BY r.id
) select r.*
  from rcps_recipe r join recipe_comments rc on r.id = rc.id
  order by comment_num desc
'''


def most_commented_recipes(limit=0):
    query = _most_commented_recipes_query
    if limit:
        query += 'limit {}'.format(limit)
    return Recipe.objects.raw(query)