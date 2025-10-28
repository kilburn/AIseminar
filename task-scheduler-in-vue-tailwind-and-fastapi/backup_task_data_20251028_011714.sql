--
-- PostgreSQL database dump
--

\restrict F2vuVNrTEu7TC6DIHFOBDaVO8WXkVmHgA4gvN74m0UaDdjME9g5H88eA7ZGN6Fw

-- Dumped from database version 15.14
-- Dumped by pg_dump version 15.14

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: scheduler
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO scheduler;

--
-- Name: task; Type: TABLE; Schema: public; Owner: scheduler
--

CREATE TABLE public.task (
    id integer NOT NULL,
    "createdDate" timestamp without time zone,
    "dueDate" timestamp without time zone,
    title character varying(50),
    description text,
    status character varying(50)
);


ALTER TABLE public.task OWNER TO scheduler;

--
-- Name: task_id_seq; Type: SEQUENCE; Schema: public; Owner: scheduler
--

CREATE SEQUENCE public.task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_id_seq OWNER TO scheduler;

--
-- Name: task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: scheduler
--

ALTER SEQUENCE public.task_id_seq OWNED BY public.task.id;


--
-- Name: task id; Type: DEFAULT; Schema: public; Owner: scheduler
--

ALTER TABLE ONLY public.task ALTER COLUMN id SET DEFAULT nextval('public.task_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: scheduler
--

COPY public.alembic_version (version_num) FROM stdin;
1934c2ec8b3d
\.


--
-- Data for Name: task; Type: TABLE DATA; Schema: public; Owner: scheduler
--

COPY public.task (id, "createdDate", "dueDate", title, description, status) FROM stdin;
\.


--
-- Name: task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: scheduler
--

SELECT pg_catalog.setval('public.task_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: scheduler
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: task task_pkey; Type: CONSTRAINT; Schema: public; Owner: scheduler
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict F2vuVNrTEu7TC6DIHFOBDaVO8WXkVmHgA4gvN74m0UaDdjME9g5H88eA7ZGN6Fw

