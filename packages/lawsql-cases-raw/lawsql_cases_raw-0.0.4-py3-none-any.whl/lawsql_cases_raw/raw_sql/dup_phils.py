duplicate_phil_reports = """--sql
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
        phil,
        count(*)
    from
        Decisions
    where
        phil is not null
    group by
        phil
    having
    count(*) > 1
  ) x on d.phil = x.phil
where d.phil is not null
order by
  d.date_prom desc;
"""
