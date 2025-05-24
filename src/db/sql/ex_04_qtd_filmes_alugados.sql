SELECT
	city.city AS cidade,
	film.film_id,
	film.title,
	COUNT(rental.rental_id) AS total_alugueis
FROM
	rental
JOIN inventory ON
	rental.inventory_id = inventory.inventory_id
JOIN film ON
	inventory.film_id = film.film_id
JOIN customer ON
	rental.customer_id = customer.customer_id
JOIN address ON
	customer.address_id = address.address_id
JOIN city ON
	address.city_id = city.city_id
GROUP BY
	city.city,
	film.film_id,
	film.title
ORDER BY
	total_alugueis DESC;