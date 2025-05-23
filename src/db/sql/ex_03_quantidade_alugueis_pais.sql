    --Quantidade de alugueis por pais
    SELECT
        co.country,
        COUNT(r.rental_id) AS total_rentals
    FROM
        rental r
    JOIN customer c ON
        r.customer_id = c.customer_id
    JOIN address a ON
        c.address_id = a.address_id
    JOIN city ci ON
        a.city_id = ci.city_id
    JOIN country co ON
        ci.country_id = co.country_id
    GROUP BY
        co.country
    ORDER BY
        total_rentals DESC