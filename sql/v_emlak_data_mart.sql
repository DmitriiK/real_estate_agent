
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
    --
	--where  eml.price/ eml.sqm_netsqm between 40 and 500


	 


	