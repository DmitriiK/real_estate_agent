
-- drop view v_emlak_data_mart
-- select * from v_emlak_data_mart
create or replace view v_emlak_data_mart as 
select  eml.id, 
	eml.createdate, 
  	eml.city_id,  dc.city_name
   ,eml.country_id, c.country_name
   ,eml.district_id,  d.district_name, 
	rc.room,  rc.living_room as livingroom
	,eml.room_category_id, rc.room_category 
	,dft.floor_type_name , eml.floor_count,
	is_furnished,  
	eml.price , eml.sqm_netsqm, 
	--eml.maplocation_lat, eml.maplocation_lon,
	eml.age, 
	concat('https://www.hepsiemlak.com/', fd.detailurl) as detailurl,
	--cast(1.0*ec.dist_to_sea/1000 as decimal(6,1)) as dist_to_sea,
	calc.sqm_price
	from  public.f_emlak eml
	join d_countries c on c.country_id =eml.country_id
	join d_districts d on d.district_id =eml.district_id
	join d_cities dc on dc.city_id =eml.city_id 
	join d_floor_type dft on dft.floor_type_id =eml.floor_type_id 
	left join v_room_category rc on rc.room_category_id=eml.room_category_id
	left join f_emlak_details fd on fd.id = eml.id
	--left join public.f_emlak_calc ec  on eml.id=ec.id 
	,
	lateral (select eml.price/eml.sqm_netsqm as sqm_price) calc;

	--where  eml.price/ eml.sqm_netsqm between 40 and 500
    -- 
COMMENT ON COLUMN v_emlak_data_mart.id IS 'Primary identifier for the real estate property';
COMMENT ON COLUMN v_emlak_data_mart.createdate IS 'Date when the property record was created';
COMMENT ON COLUMN v_emlak_data_mart.city_id IS 'Foreign key referencing d_cities.city_id';
COMMENT ON COLUMN v_emlak_data_mart.city_name IS 'Name of the province("ile" in Turkey) where the property is located, like Antalya, Izmir, ';
COMMENT ON COLUMN v_emlak_data_mart.country_id IS 'Foreign key referencing d_countries.country_id';
COMMENT ON COLUMN v_emlak_data_mart.country_name IS 'Name of the district of the city, like Kepez, Konyaalti for Antalya city,  where the property is located';
COMMENT ON COLUMN v_emlak_data_mart.district_id IS 'Foreign key referencing d_districts.district_id';
COMMENT ON COLUMN v_emlak_data_mart.district_name IS 'Name of the local district (mahalle in Turkey), like "Liman" for Koniyaalti district, where the property is located';
COMMENT ON COLUMN v_emlak_data_mart.room IS 'Number of bed rooms in the property';
COMMENT ON COLUMN v_emlak_data_mart.livingroom IS 'Number of living rooms in the property. Living room usually big room with kitchen in Turkey';
COMMENT ON COLUMN v_emlak_data_mart.floor_type_name IS 'Type of floor the property is on (e.g., ground floor, first floor)';
COMMENT ON COLUMN v_emlak_data_mart.floor_count IS 'Total number of floors in the building';
COMMENT ON COLUMN v_emlak_data_mart.is_furnished IS 'Boolean indicating whether the property is furnished';
COMMENT ON COLUMN v_emlak_data_mart.price IS 'Price of the property in turkish lira';
COMMENT ON COLUMN v_emlak_data_mart.sqm_netsqm IS 'Net square meters of the property';

COMMENT ON COLUMN v_emlak_data_mart.sqm_price IS 'Price per square meter (calculated as price divided by net square meters)';
COMMENT ON COLUMN v_emlak_data_mart.room_category_id IS 'Foreign key referencing the room category dimension';
COMMENT ON COLUMN v_emlak_data_mart.room_category IS 'Description of the room category, format "N+L", like "2+1" means an apartment with 2 bedrooms plus 1 living room. Living room usually a kitchen  ';

COMMENT ON COLUMN v_emlak_data_mart.detailurl IS 'URL, link to the page with details of estate property';



	 


	