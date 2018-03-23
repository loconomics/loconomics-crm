use loco_sales;
create table yelp_load (
   id int primary key auto_increment,
   phone varchar(255),
   yelp_id varchar(255),
   yelp_url varchar(255),
   business_name varchar(255),
   address varchar(255),
   city varchar(255),
   state varchar(255),
   zip_code varchar(255),
   yelp_top_category varchar(255),
   yelp_review_count varchar(255),
   yelp_rating varchar(255),
   yelp_url_scraped int(1) default 0   
);
alter table yelp_load add unique k_yi(yelp_id);

create table yelp_load_emails (
   id int primary key auto_increment,
   yelp_load_id int NOT NULL,
   domain varchar(255),
   email varchar(255)
);

create table bing_registered_load (
   id int primary key auto_increment,
   bing_url varchar(50),

);

create table registered_biz (
   location_id varchar(255),
   business_account varchar(255),
   ownership_name varchar(255),
   dba_name varchar(255),
   street_address varchar(255),
   city varchar(255),
   state varchar(255),
   source_zip varchar(255),
   biz_start_date varchar(255),
   biz_end_date varchar(255),
   location_start_date varchar(255),
   location_end_date varchar(255),
   mail_address varchar(255),
   mail_city varchar(255),
   mail_zip varchar(255),
   mail_state varchar(255),
   naics_code varchar(255),
   parking_tax varchar(255),
   transient_occupancy_tax varchar(255),
   lic_code varchar(255),
   lic_code_description varchar(255),
   supervisor varchar(255),
   neighborhoods varchar(255),
   business_corridor varchar(255),
   business_location varchar(255)
);
