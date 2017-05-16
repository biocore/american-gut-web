-- May 16, 2017
-- Add an admin user for labadmin with highest access levels to ease manual
-- debugging

-- create new user 'master'
INSERT INTO ag.labadmin_users (email, password)
VALUES ('master',
	      '$2a$10$2.6Y9HmBqUFmSvKCjWmBte70WF.zd3h4VqbhLMQK1xP67Aj3rei86');

-- set priviledges for 'master' to highest level
INSERT INTO ag.labadmin_users_access (access_id, email) VALUES (7, 'master');
