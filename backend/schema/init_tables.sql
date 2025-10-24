-- Create the database (run as admin if database doesn't already exist)-- Create the database (run as admin if database doesn't already exist)

-- CREATE DATABASE readingtracker;--



-- Create schema/tables for the Reading Tracker app-- Create schema/tables for the Reading Tracker app

CREATE TABLE IF NOT EXISTS public.book (CREATE TABLE IF NOT EXISTS public.book (

  id SERIAL PRIMARY KEY,  id SERIAL PRIMARY KEY,

  title VARCHAR(120) NOT NULL,  title VARCHAR(120) NOT NULL,

  author VARCHAR(120) NOT NULL,  author VARCHAR(120) NOT NULL,

  total_pages INTEGER NOT NULL,  total_pages INTEGER NOT NULL,

  status VARCHAR(20) NOT NULL DEFAULT 'To be read'  status VARCHAR(20) NOT NULL DEFAULT 'To be read'

););



CREATE TABLE IF NOT EXISTS public.reading_log (CREATE TABLE IF NOT EXISTS public.reading_log (

  id SERIAL PRIMARY KEY,  id SERIAL PRIMARY KEY,

  book_id INTEGER NOT NULL REFERENCES public.book(id) ON DELETE CASCADE,  book_id INTEGER NOT NULL REFERENCES public.book(id) ON DELETE CASCADE,

  date DATE NOT NULL,  date DATE NOT NULL,

  pages_read INTEGER NOT NULL  pages_read INTEGER NOT NULL

););
