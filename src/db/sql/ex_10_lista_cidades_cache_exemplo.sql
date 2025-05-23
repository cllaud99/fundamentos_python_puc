SELECT
    DISTINCT
        c.city,
        a.district,
        c2.country 
FROM
	address a 
JOIN
	city c ON
	c.city_id = a.city_id 
JOIN
	country c2 ON
	c2.country_id = c.country_id 