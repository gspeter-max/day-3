
-- leetcode problem (1251. Average Selling Price)
with temp_temp as (
    select p.product_id,
        p.price,
        u.units,
        p.price * u.units as revenue 
    from product p
    join unnits s on p.product_id = u.product_id and u.purchase_date between p.start_date
    and p.end_date 
        
), 
temp_temp_2 as (
    select product_id, 
        sum(units) as total_units,
        sum(revenue) as total_revenue
    from temp_temp 
    group by product_id
)
select product_id,
    round (
        case 
            when total_units = 0 then 0 
            when total_units is null then 0 
            else total_revenue / total_units 
        end , 2) as average_price

-- leetcode problem (1280. Students and Examinations) 

with temp_temp as (
    select student_id, 
        student_name,
        subject_name
    from students 
    cross  join subjects 
),
temp_temp_2 as (
    select student_id,
        subject_name,
        count(* ) as attended_exams
    from examinations 
    group by student_id, subject_name
)
select student_id,
    student_name,
    subject_name,
    coalesce(attended_exams, 0) as attended_exams 
from temp_temp t1
left join temp_temp_2 t2
    on t1.student_id = t2.student_id and t1.subject_name = t2.subject_name 
order by student_id, subject_name; 




-- leetcode problem ( 1321. Restaurant Growth ) 

with temp_temp as (
    select visited_on,
        sum(amount) as amount 
        from customers 
        group by visited_on
), 
temp_temp _2 as (
    select visited_on,
        sum(amount) over(order by visited_on rows between 6 preceding and current row) as amount,
        round( avg(amount) over(order by visited_on rows between 6 preceding and current row),2) as average_price
    from temp_temp 
)
select visited_on,
    amount,
    average_price
from temp_temp_2
where visited_on >= date_add(select min(visited_on) from temp_temp, interval 6 day)
order by visited_on; 


-- complted 3 problems 
