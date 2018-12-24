
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  miles_biked FLOAT,
  average_speed FLOAT,
  max_speed FLOAT,
  calories_burned FLOAT,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE bike (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  manufacturer VARCHAR(255) NOT NULL
);

CREATE TABLE user_bike (
  user_id INTEGER NOT NULL,
  bike_id integer NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (bike_id) REFERENCES bike (id)
);

CREATE TABLE tag(
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	title VARCHAR(255) NOT NULL
);

CREATE TABLE post_tag(
	post_id INTEGER NOT NULL,
	tag_id INTEGER NOT NULL,
	FOREIGN KEY (post_id) REFERENCES post (id),
  	FOREIGN KEY (tag_id) REFERENCES tag (id)
)

CREATE TABLE statistics(
	user_id INTEGER NOT NULL,
	post_id INTEGER NOT NULL,
	add miles_biked FLOAT,
	add average_speed FLOAT,
	add max_speed FLOAT,
	add calories_burned FLOAT;
	FOREIGN KEY (user_id) REFERENCES user (id),
	FOREIGN KEY (post_id) REFERENCES post (id)
);
