
  create view "ecommerce_pipeline"."public"."mart_revenue__dbt_tmp"
    
    
  as (
    with orders as (
    select * from "ecommerce_pipeline"."public"."int_orders_enriched"
)
select
    date_trunc('day', purchased_at)  as order_date,
    count(order_id)                  as total_orders,
    sum(total_payment)               as total_revenue,
    avg(total_payment)               as avg_order_value,
    sum(case when order_status = 'delivered' then 1 else 0 end) as delivered_orders,
    sum(case when order_status = 'cancelled' then 1 else 0 end) as cancelled_orders
from orders
where purchased_at is not null
group by 1
order by 1
  );