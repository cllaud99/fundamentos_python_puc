--Tempo medio de aluguel por cidade dias
SELECT
    c2.city,
    AVG(EXTRACT(EPOCH FROM (r.return_date - r.rental_date)) / 86400) AS tempo_medio_aluguel_dias
FROM
    rental r
JOIN
    customer c ON c.customer_id = r.customer_id
JOIN
    address a ON a.address_id = c.address_id
JOIN
    city c2 ON c2.city_id = a.city_id
GROUP BY
    c2.city
ORDER BY
    tempo_medio_aluguel_dias DESC