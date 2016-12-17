-- Database name: foodonwheels


-- Users start here
insert into "User" values ('paul@gmail.com', 'Paul', 'F', 'Lee', 'pass', '09061234567', 'address1', True, True, True);
insert into "User" values ('chezlvan@gmail.com', 'Chezl', 'C', 'Salomon', 'pass2', '09061434597', 'address2', True, True, True);
insert into "User" values ('shannoncates@gmail.com', 'Shannon', 'E', 'Teves', 'pass3', '09063234067', 'address3', True, True, True);
-- Users end here


-- Locations start here
insert into "Location" values (1, 'Cebu City');
insert into "Location" values (2, 'Manila City');
insert into "Location" values (3, 'Cagayan de Oro City');
insert into "Location" values (4, 'Iligan City');
insert into "Location" values (5, 'Makati City');
-- Locations end here


-- Restaurants start here
insert into "Restaurant" values (1, 1, 'Pancake House', 'info1', 'address1', 'contact1');
insert into "Restaurant" values (2, 1, 'Garden Cafe', 'info2', 'address2', 'contact2');
insert into "Restaurant" values (3, 1, 'Feria', 'info3', 'address3', 'contact3');
insert into "Restaurant" values (4, 1, 'Cafe Marco', 'info4', 'address4', 'contact4');
insert into "Restaurant" values (5, 1, 'Anzani', 'info5', 'address5', 'contactno5');
insert into "Restaurant" values (6, 2, 'Greenwich', 'info6', 'address6', 'contactno6');
insert into "Restaurant" values (7, 2, 'Vikings', 'info7', 'address7', 'contactno7');
insert into "Restaurant" values (8, 2, 'Sambo Kojin', 'info8', 'address8', 'contactno8');
insert into "Restaurant" values (9, 3, 'High Ridge', 'info9', 'address9', 'contactno9');
insert into "Restaurant" values (10, 3, 'Misto', 'info10', 'address10', 'contact10');
insert into "Restaurant" values (11, 3, 'Grand Caprice', 'info11', 'address11', 'contact11');
insert into "Restaurant" values (12, 3, 'Yellow Cab Pizza', 'info12', 'address12', 'contact12');
insert into "Restaurant" values (13, 4, 'Pizzarella', 'info13', 'address13', 'contact13');
insert into "Restaurant" values (14, 4, 'Jollibee', 'info14', 'address14', 'contact14');
insert into "Restaurant" values (15, 4, 'Mcdo', 'info15', 'address15', 'contact15');
insert into "Restaurant" values (16, 4, 'Lai-Lai Yeoung Chow', 'info16', 'address16', 'contact16');
insert into "Restaurant" values (17, 5, 'Omakase', 'info17', 'address17', 'contact17');
insert into "Restaurant" values (18, 5, 'Lazy Bastard', 'info18', 'address18', 'contact18');
insert into "Restaurant" values (19, 5, 'Yardstick', 'info19', 'address19', 'contactno19');
insert into "Restaurant" values (20, 5, 'Sweet Ecstasy', 'info20', 'address20', 'contactno20');
-- Restaurants end here


-- Foods start here
insert into "Food" values (1, 1, 'Classic Pancakes', 'info1', 'Php 170.00');
insert into "Food" values (2, 1, 'Walnut Pancakes', 'info2', 'Php 189.00');
insert into "Food" values (3, 2, 'Garden Salad', 'info3', 'Php 150.00');
insert into "Food" values (4, 2, 'Sweet Potato Fries', 'info4', 'Php 95.00');
insert into "Food" values (5, 3, 'Penne Napolitano', 'info5', 'Php 400.00');
insert into "Food" values (6, 3, 'Four Cheese', 'info6', 'Php 450.00');
insert into "Food" values (7, 4, 'Three Egg Omelet', 'info7', 'Php 230.00');
insert into "Food" values (8, 5, 'Raspberry Salad Vinaigrette', 'info8', 'Php 418.00');
insert into "Food" values (9, 6, 'Ultimate Overload', 'info9', 'Php 289.00');
insert into "Food" values (10, 7, 'food1', 'info10', 'price10');
insert into "Food" values (11, 7, 'food2', 'info11', 'price11');
insert into "Food" values (12, 8, 'food3', 'info12', 'price12');
insert into "Food" values (13, 9, 'food4', 'info13', 'price13');
insert into "Food" values (14, 9, 'food5', 'info14', 'price14');
insert into "Food" values (15, 10, 'food6', 'info15', 'price15');
insert into "Food" values (16, 11, 'food7', 'info16', 'price16');
insert into "Food" values (17, 12, 'food8', 'info17', 'price17');
insert into "Food" values (18, 12, 'food9', 'info18', 'price18');
insert into "Food" values (19, 13, 'food10', 'info19', 'price19');
insert into "Food" values (20, 13, 'food11', 'info20', 'price20');
insert into "Food" values (21, 14, 'food12', 'info21', 'price21');
insert into "Food" values (22, 14, 'food13', 'info22', 'price22');
insert into "Food" values (23, 15, 'food14', 'info23', 'price23');
insert into "Food" values (24, 15, 'food15', 'info24', 'price24');
insert into "Food" values (25, 16, 'food16', 'info25', 'price25');
insert into "Food" values (26, 17, 'food17', 'info26', 'price26');
insert into "Food" values (27, 18, 'food18', 'info27', 'price27');
insert into "Food" values (28, 19, 'food19', 'info28', 'price28');
insert into "Food" values (29, 20, 'food20', 'info29', 'price29');
-- Foods end here