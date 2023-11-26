CREATE TABLE "User" (
  "id" integer PRIMARY KEY,
  "first_name" varchar(50),
  "last_name" varchar(50),
  "username" varchar(100),
  "email" email(255),
  "phone_number" varchar(50) UNIQUE,
  "data_joined" timestamp,
  "is_staff" boolean DEFAULT false,
  "is_active" boolean DEFAULT false
);

CREATE TABLE "UserProfile" (
  "id" integer PRIMARY KEY,
  "user" OneToOne,
  "profile_picture" image,
  "telebot_id" varchar,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "Product" (
  "id" integer PRIMARY KEY,
  "owner" ForeignKey,
  "product_name" varchar(255),
  "slug" slug,
  "description" textfield(500),
  "category" ForeignKey,
  "brand" ForeignKey,
  "attribute_value" ManyToMany,
  "rating" Decimal,
  "numReviews" integer,
  "link_youtube" varchar,
  "is_available" boolean,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "ProductImage" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "alternative_text" varchar,
  "url_image" ImageField,
  "product" ForeignKey,
  "main_image" boolean
);

CREATE TABLE "Atribute" (
  "id" integer PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "AtributeValue" (
  "id" integer PRIMARY KEY,
  "value" varchar,
  "atribute" ForeignKey
);

CREATE TABLE "Category" (
  "id" integer PRIMARY KEY,
  "category_name" varchar(50),
  "description" textfield(255)
);

CREATE TABLE "Brand" (
  "id" integer PRIMARY KEY,
  "brand_name" varchar,
  "description" textfield(255)
);

CREATE TABLE "CartItem" (
  "id" integer PRIMARY KEY,
  "cart" ForeignKey,
  "product" FloatField,
  "quantity" integer,
  "attribute_value" ForeignKey,
  "created_at" timestamp
);

CREATE TABLE "Cart" (
  "id" integer PRIMARY KEY,
  "user" OneToOne,
  "total_price" integer,
  "total_item" integer,
  "created_at" database
);

CREATE TABLE "ReviewRating" (
  "id" integer PRIMARY KEY,
  "user" ForeignKey,
  "product" ForeignKey,
  "name" varchar,
  "rating" integer,
  "comment" textfield,
  "is_available" boolean,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "Order" (
  "id" integer PRIMARY KEY,
  "user" ForeignKey,
  "payment_method" varchar,
  "order_number" varchar,
  "order_note" varchar,
  "total_price" Decimal,
  "shipping_price" Decimal,
  "tax" ForeignKey,
  "status" choise,
  "is_paid" boolean,
  "paid_at" timestamp,
  "is_delivered" boolean,
  "delivered_at" timestamp,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "Tax" (
  "id" integer PRIMARY KEY,
  "name_tax" varchar,
  "value_tax" FloatField,
  "default" boolean
);

CREATE TABLE "OrderItem" (
  "id" integer PRIMARY KEY,
  "order" ForeignKey,
  "product" ForeignKey,
  "quantity" integer,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "ShippingAdress" (
  "id" integer PRIMARY KEY,
  "order" OneToOne,
  "address" varchar,
  "country" varchar,
  "oblast" varchar,
  "city" varchar,
  "depart_num" varchar,
  "created_at" timestamp
);

CREATE TABLE "SpamEmail" (
  "id" integer PRIMARY KEY,
  "user" ForeignKey,
  "is_active" boolean,
  "created_at" timestamp
);

CREATE TABLE "News" (
  "id" integer PRIMARY KEY,
  "title" varchar,
  "image" image,
  "text" varchar,
  "created_at" timestamp
);

CREATE TABLE "Main" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "text" varchar
);

CREATE TABLE "About" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "text" varchar
);

CREATE TABLE "Licence" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "text" varchar
);

ALTER TABLE "UserProfile" ADD FOREIGN KEY ("user") REFERENCES "User" ("id");

ALTER TABLE "Product" ADD FOREIGN KEY ("owner") REFERENCES "User" ("id");

ALTER TABLE "Order" ADD FOREIGN KEY ("user") REFERENCES "User" ("id");

ALTER TABLE "ReviewRating" ADD FOREIGN KEY ("user") REFERENCES "User" ("id");

ALTER TABLE "Cart" ADD FOREIGN KEY ("user") REFERENCES "User" ("id");

ALTER TABLE "SpamEmail" ADD FOREIGN KEY ("user") REFERENCES "User" ("id");

ALTER TABLE "ReviewRating" ADD FOREIGN KEY ("product") REFERENCES "Product" ("id");

ALTER TABLE "Product" ADD FOREIGN KEY ("category") REFERENCES "Category" ("id");

ALTER TABLE "AtributeValue" ADD FOREIGN KEY ("atribute") REFERENCES "Atribute" ("id");

CREATE TABLE "AtributeValue_Product" (
  "AtributeValue_id" integer,
  "Product_attribute_value" ManyToMany,
  PRIMARY KEY ("AtributeValue_id", "Product_attribute_value")
);

ALTER TABLE "AtributeValue_Product" ADD FOREIGN KEY ("AtributeValue_id") REFERENCES "AtributeValue" ("id");

ALTER TABLE "AtributeValue_Product" ADD FOREIGN KEY ("Product_attribute_value") REFERENCES "Product" ("attribute_value");


ALTER TABLE "CartItem" ADD FOREIGN KEY ("attribute_value") REFERENCES "AtributeValue" ("id");

ALTER TABLE "ProductImage" ADD FOREIGN KEY ("product") REFERENCES "Product" ("id");

ALTER TABLE "OrderItem" ADD FOREIGN KEY ("product") REFERENCES "Product" ("id");

ALTER TABLE "CartItem" ADD FOREIGN KEY ("product") REFERENCES "Product" ("id");

ALTER TABLE "OrderItem" ADD FOREIGN KEY ("order") REFERENCES "Order" ("id");

ALTER TABLE "Product" ADD FOREIGN KEY ("brand") REFERENCES "Brand" ("id");

ALTER TABLE "Order" ADD FOREIGN KEY ("tax") REFERENCES "Tax" ("id");

ALTER TABLE "ShippingAdress" ADD FOREIGN KEY ("order") REFERENCES "Order" ("id");

ALTER TABLE "CartItem" ADD FOREIGN KEY ("cart") REFERENCES "Cart" ("id");
