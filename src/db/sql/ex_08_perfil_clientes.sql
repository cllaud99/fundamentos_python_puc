SELECT
	customer.customer_id,
	CONCAT(customer.first_name, ' ', customer.last_name) AS nome_completo,
	city.city AS cidade,
	address.district AS estado,
	country.country AS pais,
	COALESCE(SUM(payment.amount), 0) AS gasto_total
FROM
	customer
JOIN address ON
	customer.address_id = address.address_id
JOIN city ON
	address.city_id = city.city_id
JOIN country ON
	country.country_id = city.country_id 
LEFT JOIN rental ON
	customer.customer_id = rental.customer_id
LEFT JOIN payment ON
	rental.rental_id = payment.rental_id
GROUP BY
	customer.customer_id,
	customer.first_name,
	customer.last_name,
	address.district,
	country.country,
	city.city
ORDER BY
	customer.customer_id;
