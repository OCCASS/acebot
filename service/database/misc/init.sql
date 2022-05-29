INSERT INTO public.gender (id, name) VALUES (1, 'Парень');
INSERT INTO public.gender (id, name) VALUES (2, 'Девушка');
INSERT INTO public.game (id, name) VALUES (1, 'PUBG Mobile');
INSERT INTO public.game (id, name) VALUES (2, 'PUBG New State');
SELECT setval('city_id_seq', (SELECT MAX(id) FROM city) + 1);
SELECT setval('country_id_seq', (SELECT MAX(id) FROM country) + 1);
