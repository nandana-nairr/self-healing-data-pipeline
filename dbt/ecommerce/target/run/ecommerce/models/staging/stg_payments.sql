
  create view "ecommerce_pipeline"."public"."stg_payments__dbt_tmp"
    
    
  as (
    with source as (
    select * from "ecommerce_pipeline"."public"."raw_payments"
),
renamed as (
    select
        order_id,
        payment_sequential,
        payment_type,
        payment_installments,
        payment_value::numeric(10,2) as payment_value
    from source
    where payment_value > 0
)
select * from renamed
  );