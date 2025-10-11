create database Chococruch;
use Chococruch;
create table product_info(
product_code varchar(30) primary key,
product_name TEXT,
brand TEXT
);
show tables;
select count(*) from product_info;
drop table nutrient_info;
select count(distinct product_code) from product_info;


create table nutrient_info(
product_code varchar(30),
energy_kcal_value float,
energy_kj_value float,
carbohydrates_value float,
sugars_value float,
fat_value float,
saturated_fat_value float,
proteins_value float,
salt_value float, 
sodium_value float,
fruits_vegetables_nuts_estimate_from_ingredients_100g float,
nutrition_score_fr int,
nova_group int,
foreign key (product_code) references product_info(product_code)
);

select * from nutrient_info;


create table derived_metrics(
product_code varchar(30),
sugar_to_carb_ratio Float,
calorie_category TEXT,
sugar_category TEXT,
is_ultra_processed TEXT,
foreign key (product_code) references product_info(product_code)
);

select * from derived_metrics;

select * from product_info;


-- Product Info
-- 1)Count products per brand
select brand,count(product_name) totproducts from product_info group by brand order by totproducts desc;

-- 2)Count unique products per brand
select brand,count(distinct product_name) uniquetotproducts from product_info group by brand order by uniquetotproducts desc;

-- 3)Top 5 brands by product count
select brand Brand,count(product_name) `Count of Products` from product_info group by brand order by `Count of Products` desc Limit 5;

-- 4)Products with missing product name


-- 5)Number of unique brands
select count(distinct brand) `Unique Brands` from product_info;

-- 6)Products with code starting with '3'
select product_name from product_info where product_code like '3%';


-- nutrient_info
-- 1)Top 10 products with highest energy-kcal_value
select p.product_name,n.energy_kcal_value from product_info p join nutrient_info n on n.product_code=p.product_code order by energy_kcal_value desc limit 10;

-- 2)Average sugars_value per nova-group
select nova_group,avg(sugars_value) as Avg_Sugar_value from nutrient_info group by nova_group order by nova_group;

-- 3)Count products with fat_value > 20g
select count(p.product_name) from product_info p join nutrient_info n on n.product_code=p.product_code where n.fat_value>20;

-- 4)Average carbohydrates_value per product
select p.product_name,avg(n.carbohydrates_value) avg_carbs_value from product_info p join nutrient_info n on n.product_code=p.product_code 
group by p.product_name order by avg_carbs_value desc;

-- 5)Products with sodium_value > 1g
select p.product_name from product_info p join nutrient_info n on n.product_code=p.product_code where n.sodium_value>1;

-- 6)Count products with non-zero fruits-vegetables-nuts content
select count(product_code)as non_zero_fruits_vegetables_nuts_content from nutrient_info where fruits_vegetables_nuts_estimate_from_ingredients_100g!=0;

-- 7)Products with energy-kcal_value > 500
select p.product_name,n.energy_kcal_value from product_info p join nutrient_info n on n.product_code=p.product_code where n.energy_kcal_value>500;


-- derived_metrics
-- 1) Count products per calorie_category
select calorie_category,count(product_code) as countno from derived_metrics group by calorie_category;

-- 2)Count of High Sugar products
select sugar_category,count(product_code) from derived_metrics where sugar_category='High Sugar';

-- 3)Average sugar_to_carb_ratio for High Calorie products
select calorie_category,avg(sugar_to_carb_ratio) from derived_metrics where calorie_category='High';

-- 4) Products that are both High Calorie and High Sugar

select p.product_name from derived_metrics d join product_info p on p.product_code=d.product_code
 where d.sugar_category='High Sugar' and d.calorie_category='High'; 
 
-- 5)Number of products marked as ultra-processed
select count(product_code) from derived_metrics where is_ultra_processed='yes';

-- 6)Products with sugar_to_carb_ratio > 0.7
select p.product_name from derived_metrics d join product_info p on p.product_code=d.product_code where d.sugar_to_carb_ratio>0.7;

-- 7)Average sugar_to_carb_ratio per calorie_category
select calorie_category,avg(sugar_to_carb_ratio) from derived_metrics group by calorie_category;


-- Join Queries

-- 1)Top 5 brands with most High Calorie products
select p.brand,count(p.product_name) as high_cal_products from derived_metrics d join product_info p on p.product_code=d.product_code
 where d.calorie_category='High' group by p.brand order by high_cal_products desc limit 5;
 
 -- 2)Average energy-kcal_value for each calorie_category
select d.calorie_category,avg(n.energy_kcal_value) as avg_energy_kcal_value from derived_metrics d join product_info p on p.product_code=d.product_code
join nutrient_info n  on n.product_code=d.product_code group by d.calorie_category;

-- 3)Count of ultra-processed products per brand
select p.brand,count(d.is_ultra_processed) as count_of_ultra_processed from derived_metrics d 
join product_info p on p.product_code=d.product_code where d.is_ultra_processed='yes' group by p.brand order by count_of_ultra_processed desc;

-- 4)Products with High Sugar and High Calorie along with brand
select p.brand,p.product_name from derived_metrics d join product_info p on p.product_code=d.product_code
 where d.sugar_category='High Sugar' and d.calorie_category='High'; 
 
 -- 5)Average sugar content per brand for ultra-processed products
 select p.brand,avg(n.sugars_value) as avg_sugars_content from derived_metrics d join product_info p on p.product_code=d.product_code
join nutrient_info n  on n.product_code=d.product_code where d.is_ultra_processed='yes' group by p.brand;

-- 6)Number of products with fruits/vegetables/nuts content in each calorie_category
select d.calorie_category,count(p.product_name) as count_products from nutrient_info n 
join derived_metrics d on d.product_code=n.product_code 
join product_info p on p.product_code=n.product_code 
where n.fruits_vegetables_nuts_estimate_from_ingredients_100g>0
group by d.calorie_category; 

-- 7) Top 5 products by sugar_to_carb_ratio with their calorie and sugar category
select p.product_name,d.calorie_category,d.sugar_category,d.sugar_to_carb_ratio from nutrient_info n 
join derived_metrics d on d.product_code=n.product_code 
join product_info p on p.product_code=n.product_code
order by d.sugar_to_carb_ratio desc limit 5;







