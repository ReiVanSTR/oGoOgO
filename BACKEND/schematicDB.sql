--[[Creating main database]]--

CREATE TABLE users (
	ID int NOT NULL AUTO_INCREMENT,
	user VARCHAR(255) NOT NULL,
	status BOOLEAN DEFAULT FALSE, 
	PRIMARY KEY(ID)
);

--[[Create new user]]--
INSERT INTO  users (user) 
SELECT 'Admin' FROM DUAL 
WHERE NOT EXISTS (SELECT 1 FROM users WHERE user = 'Admin');

--[[Get User]]--
SELECT * FROM users WHERE user =%s;

--[[Updating users status]]--
UPDATE users SET status = %s
WHERE user = %s;

--[[Del user]]--
DELETE FROM users WHERE user = user (username);