-- clientes com mais de 10 transações
SELECT
    ci.city,
    COUNT(DISTINCT c.customer_id) AS num_clientes,
    COUNT(p.payment_id) AS total_transacoes_cidade
FROM city ci
    JOIN address a ON ci.city_id = a.city_id
    JOIN customer c ON a.address_id = c.address_id
    LEFT JOIN payment p ON c.customer_id = p.customer_id
GROUP BY ci.city
HAVING COUNT(p.payment_id) > 10
ORDER BY num_clientes DESC