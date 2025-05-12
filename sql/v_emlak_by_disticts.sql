
create or replace view v_emlak_by_districts as 
select 
edt.province_id, edt.province_name,   
edt.sub_province_id, edt.sub_province_name, 
edt.district_id, district_name, 
count(1) as count_of_objects
from public.v_emlak_data_mart edt
group by 
edt.province_id, edt.province_name, 
    edt.sub_province_id, 
        edt.sub_province_name, edt.district_id, district_name 