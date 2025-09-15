with mo(data) as (SELECT value FROM mm.adj WHERE (key = 'DISPLAY_NUM_FORMAT'     and section = 'IB'))

SELECT
      upper(concat_ws(' ', md.surname, md.name, md.patron)) as fio
    , md.id as mdoc_id
    , mm.mdoc_get_num_format(hd.admission_num,hd.admission_year,md.num_org,md.num_filial,md.num_type,mdtp.id,mdtp.class,data) AS ib_num
    , f.pacs_uid
FROM  mm.hospdoc AS hd
    JOIN mo on true
    JOIN mm.mdoc AS md ON md.id = hd.mdoc_id
    JOIN mm.mdoc_type mdtp ON mdtp.id = md.mdoc_type_id
    JOIN mm.people AS p ON p.id = md.people_id
    JOIN mm.ehr_case ec ON hd.ehr_case_id = ec.id
    JOIN mm.ehr_case_action ea ON ec.last_action_id = ea.id
    LEFT JOIN mm.pinfo f ON f.people_id = p.id
WHERE   hd.location_status_id = 2
    AND ea.state_value = 'active'
    AND hd.dept_id::text = :dept_id

LIMIT :limit
OFFSET :offset
