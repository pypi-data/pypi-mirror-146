duplicate_elements_of_dockets = """--sql
select
  d.pk,
  d.source,
  substr(d.case_title,0,50),
  d.cat,
  d.idx,
  d.date_prom,
  d.phil,
  d.scra
from
  Decisions d
  join (
    select
      cat,
      idx,
      date_prom,
      count(*)
    from
      Decisions d
    where
      cat is not null
      and idx is not null and d.idx != ''
    group by
      cat,
      idx,
      date_prom
    having
      count(*) > 1
  ) x on (
    d.cat = x.cat
    and d.idx = x.idx
    and d.date_prom = x.date_prom
  )
where d.cat is not null
      and d.idx is not null and d.idx != ''
order by
  d.date_prom desc;
"""
