--
-- PostgreSQL database dump
--

-- Dumped from database version 12.11 (Ubuntu 12.11-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.11 (Ubuntu 12.11-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP INDEX public.ts_idx;
ALTER TABLE ONLY public.pictures DROP CONSTRAINT pictures_url_key;
ALTER TABLE ONLY public.pictures DROP CONSTRAINT pictures_pkey;
ALTER TABLE public.pictures ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE public.pictures_id_seq;
DROP TABLE public.pictures;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: pictures; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pictures (
    id integer NOT NULL,
    name text NOT NULL,
    url text,
    exif text,
    obj_name text,
    ts tsvector GENERATED ALWAYS AS (to_tsvector('english'::regconfig, exif)) STORED
);


--
-- Name: pictures_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pictures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: pictures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pictures_id_seq OWNED BY public.pictures.id;


--
-- Name: pictures id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pictures ALTER COLUMN id SET DEFAULT nextval('public.pictures_id_seq'::regclass);


--
-- Data for Name: pictures; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.pictures (id, name, url, exif, obj_name) FROM stdin;
9	dog	https://r26-pixly-bucket-rs.s3.us-west-2.amazonaws.com/iu.jpg	{"ResolutionUnit": "2", "ExifOffset": "90", "Orientation": "1", "XResolution": "300.0", "YResolution": "300.0"}	iu.jpg
14	mountain	https://r26-pixly-bucket-rs.s3.us-west-2.amazonaws.com/pic1.jpg	{"ResolutionUnit": "2", "ExifOffset": "102", "Orientation": "1", "YCbCrPositioning": "1", "XResolution": "25.4", "YResolution": "25.4"}	pic1.jpg
15	sanowman	https://r26-pixly-bucket-rs.s3.us-west-2.amazonaws.com/0.png	{}	0.png
16	snowman	https://r26-pixly-bucket-rs.s3.us-west-2.amazonaws.com/3.png	{}	3.png
17	snowman	https://r26-pixly-bucket-rs.s3.us-west-2.amazonaws.com/5.png	{}	5.png
18	dog	https://r26-pixly-bucket-rs.s3.us-west-2.amazonaws.com/1.png	{}	1.png
\.


--
-- Name: pictures_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.pictures_id_seq', 18, true);


--
-- Name: pictures pictures_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pictures
    ADD CONSTRAINT pictures_pkey PRIMARY KEY (id);


--
-- Name: pictures pictures_url_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pictures
    ADD CONSTRAINT pictures_url_key UNIQUE (url);


--
-- Name: ts_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ts_idx ON public.pictures USING gin (ts);


--
-- PostgreSQL database dump complete
--

