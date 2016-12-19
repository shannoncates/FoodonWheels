-- Database name: foodonwheels


-- Users start here
insert into "User" values (1, 'paul@gmail.com', 'Paul', 'F', 'Lee', 'pass', '09061234567', 'address1', True, True, True);
insert into "User" values (2, 'chezlvan@gmail.com', 'Chezl', 'C', 'Salomon', 'pass2', '09061434597', 'address2', True, True, True);
insert into "User" values (3, 'shannoncates@gmail.com', 'Shannon', 'E', 'Teves', 'pass3', '09063234067', 'address3', True, True, True);
-- Users end here


-- Locations start here
insert into "Location" values (1, 'Cebu City');
insert into "Location" values (2, 'Manila City');
insert into "Location" values (3, 'Iligan City');
-- Locations end here


-- Restaurants start here
insert into "Restaurant" values (1, 1, 'Pancake House', 'info1', 'address1', 'contact1');
insert into "Restaurant" values (2, 1, 'Greenwich', 'info2', 'address2', 'contact2');
insert into "Restaurant" values (3, 1, 'Feria', 'info3', 'address3', 'contact3');
insert into "Restaurant" values (4, 1, 'Cafe Marco', 'info4', 'address4', 'contact4');
insert into "Restaurant" values (5, 1, 'Anzani', 'info5', 'address5', 'contactno5');
insert into "Restaurant" values (6, 2, 'Garden Cafe', 'info6', 'address6', 'contactno6');
insert into "Restaurant" values (7, 2, 'Vikings', 'info7', 'address7', 'contactno7');
insert into "Restaurant" values (8, 2, 'Sambo Kojin', 'info8', 'address8', 'contactno8');
insert into "Restaurant" values (9, 3, 'Pizzarella', 'info13', 'address13', 'contact13');
insert into "Restaurant" values (10, 3, 'Jollibee', 'info14', 'address14', 'contact14');
insert into "Restaurant" values (11, 3, 'Mcdo', 'info15', 'address15', 'contact15');
insert into "Restaurant" values (12, 3, 'Lai-Lai Yeoung Chow', 'info16', 'address16', 'contact16');

-- Restaurants end here


-- Foods start here
insert into "Food" values (1, 1, 'Classic Pancakes', 'Php 170.00');
insert into "Food" values (2, 1, 'Walnut Pancakes', 'Php 189.00');
insert into "Food" values (3, 1, 'Cheese Pancakes', 'Php 170.00');
insert into "Food" values (4, 1, 'Banana Pancakes', 'Php 195.00');
insert into "Food" values (5, 1, 'Bacon Waffle', 'Php 199.00');
insert into "Food" values (6, 1, 'Potato Salad', 'Php 145.00');
insert into "Food" values (7, 1, 'Children Classic Ala Carte', 'Php 100.00');
insert into "Food" values (8, 1, 'Hot Cappuccino', 'Php 90.00');
insert into "Food" values (9, 2, 'Hawaiian Pizza', 'Php 215.00');
insert into "Food" values (10, 2, 'Crispy Thins Pepperoni', 'Php 215.00');
insert into "Food" values (10, 2, 'Garden Fresh', 'Php 229.00');
insert into "Food" values (10, 2, '7 Cheese', 'Php 225.00');
insert into "Food" values (10, 2, 'Chicken Meals', 'Php 100.00');
insert into "Food" values (10, 2, 'Overloaded Meal 3', 'Php 139.00');
insert into "Food" values (10, 2, 'Pepperoni Classic', 'Php 419.00');
insert into "Food" values (10, 2, 'Ham & Cheese Classic', 'Php 299.00');
insert into "Food" values (11, 3, 'Penne Napolitano', 'Php 400.00');
insert into "Food" values (12, 3, 'Four Cheese', 'Php 450.00');
insert into "Food" values (13, 4, 'Three Egg Omelet', 'Php 230.00');
insert into "Food" values (14, 5, 'Raspberry Salad Vinaigrette', 'Php 418.00');
insert into "Food" values (15, 6, 'Garden Salad', 'Php 150.00');
insert into "Food" values (16, 7, 'food1', 'price10');
insert into "Food" values (17, 7, 'food2', 'price11');
insert into "Food" values (18, 8, 'food3', 'price12');
insert into "Food" values (19, 9, 'food10', 'price19');
insert into "Food" values (20, 9, 'food11', 'price20');
insert into "Food" values (21, 10, 'food12', 'price21');
insert into "Food" values (22, 10, 'food13', 'price22');
insert into "Food" values (23, 11, 'food14', 'price23');
insert into "Food" values (24, 11, 'food15', 'price24');
insert into "Food" values (25, 12, 'food16', 'price25');

-- Foods end here