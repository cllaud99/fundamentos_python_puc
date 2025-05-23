--Receita bruta por pais
SELECT
    c3.country AS country_name,
    SUM(p.amount) AS amount
FROM
    payment p
JOIN
    customer c ON c.customer_id = p.customer_id 
JOIN
    address a ON a.address_id = c.address_id
JOIN
    city c2 ON c2.city_id = a.city_id
JOIN
    country c3 ON c3.country_id = c2.country_id 
GROUP BY
    c3.country