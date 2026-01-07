### ENTITY: customers
**Purpose:** Stores customer information

**Attributes:**
- `customer_id`: Unique identifier for each customer (Primary Key)
- `first_name`: Customer's first name
- `last_name`: Customer's last name
- `email`: Customer's email address (must be unique)
- `phone`: Contact number of the customer
- `city`: City where the customer resides
- `registration_date`: Date when the customer registered

**Relationships:**
- One customer can place MANY orders (1:M relationship with `orders` table)
- Through orders, one customer can be linked to MANY order items (indirect relationship with `order_items` table)

### ENTITY: products
**Purpose:** Stores information about products available for sale

**Attributes:**
- `product_id`: Unique identifier for each product (Primary Key)
- `product_name`: Name of the product
- `category`: Category to which the product belongs
- `price`: Price of the product
- `stock_quantity`: Number of units available in inventory

**Relationships:**
- One product can appear in MANY order items (1:M relationship with `order_items` table)


### ENTITY: orders
**Purpose:** Stores information about customer orders

**Attributes:**
- `order_id`: Unique identifier for each order (Primary Key)
- `customer_id`: Unique identifier for the customer placing the order (Foreign Key referencing `customers.customer_id`)
- `order_date`: Date when the order was placed
- `total_amount`: Total monetary value of the order
- `status`: Current status of the order (e.g., Pending, Completed, Cancelled)

**Relationships:**
- Each order belongs to ONE customer (M:1 relationship with `customers` table)
- One customer can place MANY orders (1:M relationship between `customers` and `orders`)
- One order can contain MANY order items (1:M relationship with `order_items` table)


### ENTITY: order_items
**Purpose:** Stores the information of the items in the orders placed

**Attributes:**
- `order_item_id`: Unique identifier for each order item (Primary Key)
- `order_id`: Unique identifier for the order (Foreign Key referencing `orders.order_id`)
- `product_id`: Unique identifier for the product (Foreign Key referencing `products.product_id`)
- `quantity`: Quantity of the product in the respective order
- `unit_price`: Price of one unit of the product at the time of order
- `subtotal`: Total amount for the order item (calculated as quantity × unit_price)

Relationships: 
  - Each order item belongs to ONE order (M:1 relationship with `orders` table)
  - Each order item refers to ONE product (M:1 relationship with `products` table)
  - One order can contain MANY order items (1:M relationship between `orders` and `order_items`)
  - One product can appear in MANY order items (1:M relationship between `products` and `order_items`)

The Fleximart database schema is designed in Third Normal Form (3NF) to ensure data integrity and eliminate redundancy. In 3NF, every non‑key attribute must depend on the primary key, and there should be no transitive dependencies. This schema satisfies those conditions because each table is structured around a single primary key, and all attributes describe only that entity.

Functional Dependencies:
- In customers, customer_id → first_name, last_name, email, phone, city, registration_date.
- In products, product_id → product_name, category, price, stock_quantity.
- In orders, order_id → customer_id, order_date, total_amount, status.
- In order_items, order_item_id → order_id, product_id, quantity, unit_price, subtotal.
These dependencies show that all non‑key attributes are fully dependent on the primary key, with no partial or transitive dependencies.


Avoidance of Anomalies:
- Update anomaly: Customer details are stored only once in the customers table. Updating a phone number requires changing it in one place, avoiding inconsistencies.
- Insert anomaly: New products can be added to the products table without requiring an order record. Similarly, customers can be registered before placing orders.
- Delete anomaly: Removing an order does not erase customer or product information, since they are stored in separate tables. This prevents accidental loss of critical data when transactional records are deleted.
By separating entities into distinct tables and linking them through foreign keys, the schema enforces referential integrity and ensures that the design is in 3NF, supporting efficient queries and reliable data management.