--with mo(data) as (SELECT value FROM mm.adj WHERE (key = 'DISPLAY_NUM_FORMAT' and section = 'IB'))

SELECT DISTINCT
      upper(concat_ws(' ', md.surname, md.name, md.patron)) AS FIO
	, md.id::text AS mdoc_id
--	, mm.mdoc_get_num_format(md.num, md.year, md.num_org, md.num_filial, md.num_type, mdtp.id, mdtp.class, mo.data) as ib_num
              ,case when mdtp.class = 2
                then concat_ws('-', md.num, right(md.year, -2), md.num_type)
                else concat_ws('-', md.num, md.year, md.num_type)
                end as ib_num
    , f.pacs_uid
FROM mm.mdoc md
--    JOIN mo on true
    JOIN mm.mdoc_type mdtp ON mdtp.id = md.mdoc_type_id
    JOIN mm.people p ON p.id = md.people_id
    LEFT JOIN mm.pinfo f ON f.people_id = p.id

LIMIT :limit
OFFSET :offset
