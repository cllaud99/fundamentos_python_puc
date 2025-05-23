    --Quantidade de clientes por cidade
    SELECT
        c2.city,
        c3.country,
        a.district,
        count(*) AS costumers
    FROM
        customer c 
    JOIN
        address a ON
        c.address_id = a.address_id 
    JOIN
        city c2 ON 
        c2.city_id = a.city_id 
    JOIN
        country c3 ON
        c3.country_id = c2.country_id 
    GROUP BY
        c2.city,
        a.district,
        c3.country
    ORDER BY costumers DESC