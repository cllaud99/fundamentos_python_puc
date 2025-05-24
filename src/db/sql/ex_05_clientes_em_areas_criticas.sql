SELECT
    customer.customer_id,
    address.address AS endereco,
    address.district AS estado,
    city.city AS cidade,
    country.country AS pais
FROM
    customer
JOIN address ON
    customer.address_id = address.address_id
JOIN city ON
    address.city_id = city.city_id
JOIN country ON
    city.country_id = country.country_id
ORDER BY
    customer.customer_id;