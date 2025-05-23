    --Receita bruta por cidade
    SELECT
        ci.city,
        SUM(p.amount) AS receita_bruta
    FROM city ci
        JOIN address a ON ci.city_id = a.city_id
        JOIN customer c ON a.address_id = c.address_id
        JOIN payment p ON c.customer_id = p.customer_id
    GROUP BY ci.city
    ORDER BY receita_bruta DESC