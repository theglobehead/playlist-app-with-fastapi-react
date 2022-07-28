--
-- PostgreSQL database dump
--

-- Dumped from database version 14.3
-- Dumped by pg_dump version 14.3

-- Started on 2022-07-28 11:17:03

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

--
-- TOC entry 8 (class 2615 OID 16394)
-- Name: pgagent; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA pgagent;


ALTER SCHEMA pgagent OWNER TO postgres;

--
-- TOC entry 3562 (class 0 OID 0)
-- Dependencies: 8
-- Name: SCHEMA pgagent; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA pgagent IS 'pgAgent system tables';


--
-- TOC entry 2 (class 3079 OID 16384)
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- TOC entry 3563 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


--
-- TOC entry 3 (class 3079 OID 16395)
-- Name: pgagent; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgagent WITH SCHEMA pgagent;


--
-- TOC entry 3564 (class 0 OID 0)
-- Dependencies: 3
-- Name: EXTENSION pgagent; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgagent IS 'A PostgreSQL job scheduler';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 236 (class 1259 OID 106737)
-- Name: artists; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.artists (
    artist_id integer NOT NULL,
    artist_name character varying(350),
    modified timestamp without time zone DEFAULT now(),
    created timestamp without time zone DEFAULT now(),
    is_deleted boolean DEFAULT false
);


ALTER TABLE public.artists OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 106736)
-- Name: artist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.artist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.artist_id_seq OWNER TO postgres;

--
-- TOC entry 3565 (class 0 OID 0)
-- Dependencies: 235
-- Name: artist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.artist_id_seq OWNED BY public.artists.artist_id;


--
-- TOC entry 232 (class 1259 OID 106713)
-- Name: playlists; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.playlists (
    playlist_id integer NOT NULL,
    playlist_name character varying(350),
    modified timestamp without time zone DEFAULT now(),
    created timestamp without time zone DEFAULT now(),
    is_deleted boolean DEFAULT false,
    playlist_uuid uuid DEFAULT gen_random_uuid(),
    owner_user_id integer
);


ALTER TABLE public.playlists OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 106712)
-- Name: playlists_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.playlists_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.playlists_id_seq OWNER TO postgres;

--
-- TOC entry 3566 (class 0 OID 0)
-- Dependencies: 231
-- Name: playlists_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.playlists_id_seq OWNED BY public.playlists.playlist_id;


--
-- TOC entry 234 (class 1259 OID 106724)
-- Name: songs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.songs (
    song_id integer NOT NULL,
    song_name character varying(350),
    album character varying(350),
    modified timestamp without time zone DEFAULT now(),
    created timestamp without time zone DEFAULT now(),
    is_deleted boolean DEFAULT false,
    song_uuid uuid DEFAULT gen_random_uuid()
);


ALTER TABLE public.songs OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 106723)
-- Name: song_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.song_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.song_id_seq OWNER TO postgres;

--
-- TOC entry 3567 (class 0 OID 0)
-- Dependencies: 233
-- Name: song_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.song_id_seq OWNED BY public.songs.song_id;


--
-- TOC entry 246 (class 1259 OID 106790)
-- Name: songs_in_playlists; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.songs_in_playlists (
    id integer NOT NULL,
    created timestamp without time zone DEFAULT now(),
    is_deleted boolean DEFAULT false,
    song_id integer,
    playlist_id integer
);


ALTER TABLE public.songs_in_playlists OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 106789)
-- Name: songs_in_playlists_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.songs_in_playlists_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.songs_in_playlists_id_seq OWNER TO postgres;

--
-- TOC entry 3568 (class 0 OID 0)
-- Dependencies: 245
-- Name: songs_in_playlists_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.songs_in_playlists_id_seq OWNED BY public.songs_in_playlists.id;


--
-- TOC entry 238 (class 1259 OID 106748)
-- Name: tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tags (
    tag_id integer NOT NULL,
    tag_name character varying(350),
    modified timestamp without time zone DEFAULT now(),
    created timestamp without time zone DEFAULT now(),
    is_deleted boolean DEFAULT false
);


ALTER TABLE public.tags OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 106747)
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tags_id_seq OWNER TO postgres;

--
-- TOC entry 3569 (class 0 OID 0)
-- Dependencies: 237
-- Name: tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tags_id_seq OWNED BY public.tags.tag_id;


--
-- TOC entry 240 (class 1259 OID 106759)
-- Name: tags_in_artists; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tags_in_artists (
    id integer NOT NULL,
    created timestamp without time zone DEFAULT now(),
    is_false boolean DEFAULT false,
    tag_id integer,
    artist_id integer
);


ALTER TABLE public.tags_in_artists OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 106758)
-- Name: tags_in_artists_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tags_in_artists_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tags_in_artists_id_seq OWNER TO postgres;

--
-- TOC entry 3570 (class 0 OID 0)
-- Dependencies: 239
-- Name: tags_in_artists_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tags_in_artists_id_seq OWNED BY public.tags_in_artists.id;


--
-- TOC entry 244 (class 1259 OID 106780)
-- Name: tags_in_playlists; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tags_in_playlists (
    id integer NOT NULL,
    created boolean DEFAULT false,
    is_deleted boolean DEFAULT false,
    tag_id integer,
    playlist_id integer
);


ALTER TABLE public.tags_in_playlists OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 106779)
-- Name: tags_in_playlists_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tags_in_playlists_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tags_in_playlists_id_seq OWNER TO postgres;

--
-- TOC entry 3571 (class 0 OID 0)
-- Dependencies: 243
-- Name: tags_in_playlists_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tags_in_playlists_id_seq OWNED BY public.tags_in_playlists.id;


--
-- TOC entry 242 (class 1259 OID 106770)
-- Name: tags_in_songs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tags_in_songs (
    id integer NOT NULL,
    created timestamp without time zone DEFAULT now(),
    is_deleted boolean DEFAULT false,
    tag_id integer,
    song_id integer
);


ALTER TABLE public.tags_in_songs OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 106769)
-- Name: tags_in_songs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tags_in_songs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tags_in_songs_id_seq OWNER TO postgres;

--
-- TOC entry 3572 (class 0 OID 0)
-- Dependencies: 241
-- Name: tags_in_songs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tags_in_songs_id_seq OWNED BY public.tags_in_songs.id;


--
-- TOC entry 229 (class 1259 OID 16564)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    user_uuid uuid DEFAULT gen_random_uuid(),
    user_name character varying(64),
    password_hash character varying(64),
    password_salt character varying(8),
    modified timestamp without time zone DEFAULT now(),
    created timestamp without time zone DEFAULT now(),
    is_deleted boolean DEFAULT false
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 106701)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 3573 (class 0 OID 0)
-- Dependencies: 230
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.user_id;


--
-- TOC entry 3318 (class 2604 OID 106740)
-- Name: artists artist_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artists ALTER COLUMN artist_id SET DEFAULT nextval('public.artist_id_seq'::regclass);


--
-- TOC entry 3308 (class 2604 OID 106716)
-- Name: playlists playlist_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlists ALTER COLUMN playlist_id SET DEFAULT nextval('public.playlists_id_seq'::regclass);


--
-- TOC entry 3313 (class 2604 OID 106727)
-- Name: songs song_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.songs ALTER COLUMN song_id SET DEFAULT nextval('public.song_id_seq'::regclass);


--
-- TOC entry 3335 (class 2604 OID 106793)
-- Name: songs_in_playlists id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.songs_in_playlists ALTER COLUMN id SET DEFAULT nextval('public.songs_in_playlists_id_seq'::regclass);


--
-- TOC entry 3322 (class 2604 OID 106751)
-- Name: tags tag_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags ALTER COLUMN tag_id SET DEFAULT nextval('public.tags_id_seq'::regclass);


--
-- TOC entry 3326 (class 2604 OID 106762)
-- Name: tags_in_artists id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags_in_artists ALTER COLUMN id SET DEFAULT nextval('public.tags_in_artists_id_seq'::regclass);


--
-- TOC entry 3332 (class 2604 OID 106783)
-- Name: tags_in_playlists id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags_in_playlists ALTER COLUMN id SET DEFAULT nextval('public.tags_in_playlists_id_seq'::regclass);


--
-- TOC entry 3329 (class 2604 OID 106773)
-- Name: tags_in_songs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags_in_songs ALTER COLUMN id SET DEFAULT nextval('public.tags_in_songs_id_seq'::regclass);


--
-- TOC entry 3303 (class 2604 OID 106702)
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 3254 (class 0 OID 16396)
-- Dependencies: 214
-- Data for Name: pga_jobagent; Type: TABLE DATA; Schema: pgagent; Owner: postgres
--

COPY pgagent.pga_jobagent (jagpid, jaglogintime, jagstation) FROM stdin;
9340	2022-07-27 10:39:55.365487+03	LAPTOP-NHMT311A
\.


--
-- TOC entry 3255 (class 0 OID 16405)
-- Dependencies: 216
-- Data for Name: pga_jobclass; Type: TABLE DATA; Schema: pgagent; Owner: postgres
--

COPY pgagent.pga_jobclass (jclid, jclname) FROM stdin;
\.


--
-- TOC entry 3256 (class 0 OID 16415)
-- Dependencies: 218
-- Data for Name: pga_job; Type: TABLE DATA; Schema: pgagent; Owner: postgres
--

COPY pgagent.pga_job (jobid, jobjclid, jobname, jobdesc, jobhostagent, jobenabled, jobcreated, jobchanged, jobagentid, jobnextrun, joblastrun) FROM stdin;
\.


--
-- TOC entry 3258 (class 0 OID 16463)
-- Dependencies: 222
-- Data for Name: pga_schedule; Type: TABLE DATA; Schema: pgagent; Owner: postgres
--

COPY pgagent.pga_schedule (jscid, jscjobid, jscname, jscdesc, jscenabled, jscstart, jscend, jscminutes, jschours, jscweekdays, jscmonthdays, jscmonths) FROM stdin;
\.


--
-- TOC entry 3259 (class 0 OID 16491)
-- Dependencies: 224
-- Data for Name: pga_exception; Type: TABLE DATA; Schema: pgagent; Owner: postgres
--

COPY pgagent.pga_exception (jexid, jexscid, jexdate, jextime) FROM stdin;
\.


--
-- TOC entry 3260 (class 0 OID 16505)
-- Dependencies: 226
-- Data for Name: pga_joblog; Type: TABLE DATA; Schema: pgagent; Owner: postgres
--

COPY pgagent.pga_joblog (jlgid, jlgjobid, jlgstatus, jlgstart, jlgduration) FROM stdin;
\.


--
-- TOC entry 3257 (class 0 OID 16439)
-- Dependencies: 220
-- Data for Name: pga_jobstep; Type: TABLE DATA; Schema: pgagent; Owner: postgres
--

COPY pgagent.pga_jobstep (jstid, jstjobid, jstname, jstdesc, jstenabled, jstkind, jstcode, jstconnstr, jstdbname, jstonerror, jscnextrun) FROM stdin;
\.


--
-- TOC entry 3261 (class 0 OID 16521)
-- Dependencies: 228
-- Data for Name: pga_jobsteplog; Type: TABLE DATA; Schema: pgagent; Owner: postgres
--

COPY pgagent.pga_jobsteplog (jslid, jsljlgid, jsljstid, jslstatus, jslresult, jslstart, jslduration, jsloutput) FROM stdin;
\.


--
-- TOC entry 3546 (class 0 OID 106737)
-- Dependencies: 236
-- Data for Name: artists; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.artists (artist_id, artist_name, modified, created, is_deleted) FROM stdin;
\.


--
-- TOC entry 3542 (class 0 OID 106713)
-- Dependencies: 232
-- Data for Name: playlists; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.playlists (playlist_id, playlist_name, modified, created, is_deleted, playlist_uuid, owner_user_id) FROM stdin;
1	test playlist	2022-07-21 08:17:20.219049	2022-07-21 08:17:20.219049	f	901e02ac-79eb-46fa-a483-b743b062f940	5
2	gregr	2022-07-23 22:17:30.462838	2022-07-23 22:17:30.462838	f	ef22553e-8767-4e35-b72f-9d40b7c2236c	2
5	asdfghjkl;	2022-07-24 20:51:18.327991	2022-07-24 20:51:18.327991	f	2bf951bb-b3ea-4591-8b4a-dec0116cefcc	12
6	regrgreg	2022-07-26 19:59:03.988576	2022-07-26 19:59:03.988576	f	71728edf-3df3-4bfd-8bd3-81e1d2b2da49	2
3	sgergr	2022-07-27 22:01:52.266677	2022-07-23 22:21:52.553063	t	5146fdfd-4bc7-48bf-9418-9e11379044cd	2
7	123456789	2022-07-27 22:01:57.964979	2022-07-27 11:08:12.137057	t	1fba593e-6ebc-4835-8ef7-744ed1c4b863	2
8	123456	2022-07-28 09:39:11.224199	2022-07-28 09:39:08.051316	t	cbfb1d14-7ada-4cad-a8f5-e1e71e704492	2
4	thstr	2022-07-23 22:21:56.308366	2022-07-23 22:21:56.308366	t	e44f1a92-2c12-4077-8d34-4ad05b1bc309	2
9	erthujki	2022-07-28 10:49:38.631034	2022-07-28 10:49:38.631034	f	b18c960a-c0cc-4f74-9ac4-4d160a756b9f	2
\.


--
-- TOC entry 3544 (class 0 OID 106724)
-- Dependencies: 234
-- Data for Name: songs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.songs (song_id, song_name, album, modified, created, is_deleted, song_uuid) FROM stdin;
1	Another one bites the dust	The Game	2022-07-24 16:11:58.23207	2022-07-24 16:11:58.23207	f	26d84925-e87f-4da8-8a1a-185ec60f9703
2	My life	52nd Street	2022-07-24 16:24:13.859146	2022-07-24 16:24:13.859146	f	e1ed1a47-4c70-4921-8f53-9eeb55300ab9
3	California Dreamin'	If You Can Believe Your Eyes and Ears	2022-07-24 16:24:13.859146	2022-07-24 16:24:13.859146	f	b9de76d8-e9db-4b0f-81c0-f0da4562638c
4	Je m'voyais déjà	Je m'voyais déjà	2022-07-24 16:24:13.859146	2022-07-24 16:24:13.859146	f	e286173f-0566-4409-9274-e3ba6a550d18
6	Siffler sur la colline	Joe Dassin	2022-07-24 16:24:13.859146	2022-07-24 16:24:13.859146	f	bc49c345-078a-4dc3-8963-41e44d7566d3
5	Mes emmerdes	Charles Aznavour	2022-07-24 16:24:13.859146	2022-07-24 16:24:13.859146	f	5cf5f8c3-77cb-4ff8-a6af-4d832bab1f12
\.


--
-- TOC entry 3556 (class 0 OID 106790)
-- Dependencies: 246
-- Data for Name: songs_in_playlists; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.songs_in_playlists (id, created, is_deleted, song_id, playlist_id) FROM stdin;
1	2022-07-24 16:27:05.022953	f	1	1
2	2022-07-24 16:27:05.022953	f	2	1
3	2022-07-25 11:53:01.454981	f	3	2
4	2022-07-25 11:53:01.454981	f	4	2
6	2022-07-25 11:54:22.715825	f	5	2
8	2022-07-27 12:05:31.687196	f	2	7
7	2022-07-27 11:39:33.968872	t	1	4
10	2022-07-28 10:11:45.951752	f	2	6
13	2022-07-28 10:11:56.832081	f	6	6
14	2022-07-28 10:12:00.26492	f	5	6
9	2022-07-28 10:11:41.901638	t	1	6
12	2022-07-28 10:11:52.907446	t	4	6
11	2022-07-28 10:11:49.503646	t	3	6
15	2022-07-28 10:49:17.319294	t	6	4
\.


--
-- TOC entry 3548 (class 0 OID 106748)
-- Dependencies: 238
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tags (tag_id, tag_name, modified, created, is_deleted) FROM stdin;
\.


--
-- TOC entry 3550 (class 0 OID 106759)
-- Dependencies: 240
-- Data for Name: tags_in_artists; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tags_in_artists (id, created, is_false, tag_id, artist_id) FROM stdin;
\.


--
-- TOC entry 3554 (class 0 OID 106780)
-- Dependencies: 244
-- Data for Name: tags_in_playlists; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tags_in_playlists (id, created, is_deleted, tag_id, playlist_id) FROM stdin;
\.


--
-- TOC entry 3552 (class 0 OID 106770)
-- Dependencies: 242
-- Data for Name: tags_in_songs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tags_in_songs (id, created, is_deleted, tag_id, song_id) FROM stdin;
\.


--
-- TOC entry 3539 (class 0 OID 16564)
-- Dependencies: 229
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, user_uuid, user_name, password_hash, password_salt, modified, created, is_deleted) FROM stdin;
2	45ef97b2-9b07-46ae-a78b-0cbeb3c90476	test	412e8e102162377ed27fbe2097f36473a742f3e133bd522bfaa223f99b01104a	P>:b?cC9	2022-07-19 16:28:33.535531	2022-07-19 16:28:33.535531	f
3	e8b4c1df-6ce5-4eeb-afd2-c2c5c8e926d1	test1	60321c84436c44e9b2af48e92ad1a0517376e213086471f25ebe257ee602f7a2	cDKq6+{|	2022-07-19 16:28:47.296373	2022-07-19 16:28:47.296373	f
4	d077469e-801b-4a59-8a78-266acb175141	test2	c084f3966720f4f5fa2d30b8d65c963a9e4e3edbf93ec71a57b90404b27f3c35	1Ko&&skA	2022-07-19 16:39:12.871401	2022-07-19 16:39:12.871401	f
5	3bcfe57c-9b0d-45ea-b0bf-c5341bbce409	tes4	9d0194db6aa002e23dde3ef0d0729454e85bf40188567300adeec1b8c669a0e0	Nq=4wlQr	2022-07-19 22:38:09.247559	2022-07-19 22:38:09.247559	f
6	20d93f0a-2a56-404a-b607-ee0034aac220	testing	e2f5dfc5e66ccb9e9e6dbf8604b5c4d164e2c736e762cc57d4288ead62e8c345	ntH~Q>xA	2022-07-20 17:20:50.060161	2022-07-20 17:20:50.060161	f
7	548f6913-caba-415e-865f-b0ae8a1d48bc	valters	fd5e9f18e2267dcab9f2c75d993a8d9535d6267ec21bf7831e95af071bea1210	4TBH1Jlk	2022-07-20 18:37:14.480694	2022-07-20 18:37:14.480694	f
8	c02c3763-b286-464d-8392-5bce0360ba9d	user1	eba585c8889706c7e0d0fd5af9101915dfa590f5184b83b3ab851df0d5b12ded	,$E@+2;o	2022-07-21 21:06:26.636169	2022-07-21 21:06:26.636169	f
11	fa40b093-2141-4675-a250-afe6d7a2f7ee	q5yw56y54y	83f4992e4eaa0b8862c4103d05ec2e9fef8c775825b9e6b0c9da2e7efd6e838a	l[insiIN	2022-07-22 17:40:41.265589	2022-07-22 17:40:41.265589	f
12	1619c717-bffe-4501-8e1e-a84a4cf0b7c1	abcd	b9a204f9be936afd229095bf504ab31fb93abd918c3f5f56d766118bdfc517be	tzfH~!Gv	2022-07-24 20:49:58.121536	2022-07-24 20:49:58.121536	f
\.


--
-- TOC entry 3574 (class 0 OID 0)
-- Dependencies: 235
-- Name: artist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.artist_id_seq', 1, false);


--
-- TOC entry 3575 (class 0 OID 0)
-- Dependencies: 231
-- Name: playlists_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.playlists_id_seq', 9, true);


--
-- TOC entry 3576 (class 0 OID 0)
-- Dependencies: 233
-- Name: song_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.song_id_seq', 6, true);


--
-- TOC entry 3577 (class 0 OID 0)
-- Dependencies: 245
-- Name: songs_in_playlists_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.songs_in_playlists_id_seq', 15, true);


--
-- TOC entry 3578 (class 0 OID 0)
-- Dependencies: 237
-- Name: tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tags_id_seq', 1, false);


--
-- TOC entry 3579 (class 0 OID 0)
-- Dependencies: 239
-- Name: tags_in_artists_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tags_in_artists_id_seq', 1, false);


--
-- TOC entry 3580 (class 0 OID 0)
-- Dependencies: 243
-- Name: tags_in_playlists_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tags_in_playlists_id_seq', 1, false);


--
-- TOC entry 3581 (class 0 OID 0)
-- Dependencies: 241
-- Name: tags_in_songs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tags_in_songs_id_seq', 1, false);


--
-- TOC entry 3582 (class 0 OID 0)
-- Dependencies: 230
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 12, true);


--
-- TOC entry 3375 (class 2606 OID 106745)
-- Name: artists artist_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artists
    ADD CONSTRAINT artist_pk PRIMARY KEY (artist_id);


--
-- TOC entry 3368 (class 2606 OID 106718)
-- Name: playlists playlists_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlists
    ADD CONSTRAINT playlists_pk PRIMARY KEY (playlist_id);


--
-- TOC entry 3371 (class 2606 OID 106734)
-- Name: songs song_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.songs
    ADD CONSTRAINT song_pk PRIMARY KEY (song_id);


--
-- TOC entry 3390 (class 2606 OID 106797)
-- Name: songs_in_playlists songs_in_playlists_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.songs_in_playlists
    ADD CONSTRAINT songs_in_playlists_pk PRIMARY KEY (id);


--
-- TOC entry 3381 (class 2606 OID 106767)
-- Name: tags_in_artists tags_in_artists_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags_in_artists
    ADD CONSTRAINT tags_in_artists_pk PRIMARY KEY (id);


--
-- TOC entry 3387 (class 2606 OID 106787)
-- Name: tags_in_playlists tags_in_playlists_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags_in_playlists
    ADD CONSTRAINT tags_in_playlists_pk PRIMARY KEY (id);


--
-- TOC entry 3384 (class 2606 OID 106777)
-- Name: tags_in_songs tags_in_songs_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags_in_songs
    ADD CONSTRAINT tags_in_songs_pk PRIMARY KEY (id);


--
-- TOC entry 3378 (class 2606 OID 106756)
-- Name: tags tags_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pk PRIMARY KEY (tag_id);


--
-- TOC entry 3364 (class 2606 OID 106705)
-- Name: users users_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pk PRIMARY KEY (user_id);


--
-- TOC entry 3373 (class 1259 OID 106746)
-- Name: artist_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX artist_id_uindex ON public.artists USING btree (artist_id);


--
-- TOC entry 3366 (class 1259 OID 106719)
-- Name: playlists_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX playlists_id_uindex ON public.playlists USING btree (playlist_id);


--
-- TOC entry 3369 (class 1259 OID 106735)
-- Name: song_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX song_id_uindex ON public.songs USING btree (song_id);


--
-- TOC entry 3388 (class 1259 OID 106798)
-- Name: songs_in_playlists_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX songs_in_playlists_id_uindex ON public.songs_in_playlists USING btree (id);


--
-- TOC entry 3372 (class 1259 OID 106862)
-- Name: songs_song_uuid_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX songs_song_uuid_uindex ON public.songs USING btree (song_uuid);


--
-- TOC entry 3376 (class 1259 OID 106757)
-- Name: tags_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX tags_id_uindex ON public.tags USING btree (tag_id);


--
-- TOC entry 3379 (class 1259 OID 106768)
-- Name: tags_in_artists_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX tags_in_artists_id_uindex ON public.tags_in_artists USING btree (id);


--
-- TOC entry 3385 (class 1259 OID 106788)
-- Name: tags_in_playlists_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX tags_in_playlists_id_uindex ON public.tags_in_playlists USING btree (id);


--
-- TOC entry 3382 (class 1259 OID 106778)
-- Name: tags_in_songs_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX tags_in_songs_id_uindex ON public.tags_in_songs USING btree (id);


--
-- TOC entry 3361 (class 1259 OID 106703)
-- Name: users_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX users_id_uindex ON public.users USING btree (user_id);


--
-- TOC entry 3362 (class 1259 OID 106711)
-- Name: users_name_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX users_name_uindex ON public.users USING btree (user_name);


--
-- TOC entry 3365 (class 1259 OID 106707)
-- Name: users_uuid_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX users_uuid_uindex ON public.users USING btree (user_uuid);


--
-- TOC entry 3391 (class 2606 OID 106806)
-- Name: playlists playlists_users_user_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlists
    ADD CONSTRAINT playlists_users_user_id_fk FOREIGN KEY (owner_user_id) REFERENCES public.users(user_id) ON DELETE RESTRICT;


--
-- TOC entry 3398 (class 2606 OID 106811)
-- Name: songs_in_playlists songs_in_playlists_playlists_playlist_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.songs_in_playlists
    ADD CONSTRAINT songs_in_playlists_playlists_playlist_id_fk FOREIGN KEY (playlist_id) REFERENCES public.playlists(playlist_id) ON DELETE RESTRICT;


--
-- TOC entry 3399 (class 2606 OID 106846)
-- Name: songs_in_playlists songs_in_playlists_songs_song_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.songs_in_playlists
    ADD CONSTRAINT songs_in_playlists_songs_song_id_fk FOREIGN KEY (song_id) REFERENCES public.songs(song_id);


--
-- TOC entry 3392 (class 2606 OID 106816)
-- Name: tags_in_artists tags_in_artists_artists_artist_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags_in_artists
    ADD CONSTRAINT tags_in_artists_artists_artist_id_fk FOREIGN KEY (artist_id) REFERENCES public.artists(artist_id);


--
-- TOC entry 3393 (class 2606 OID 106821)
-- Name: tags_in_artists tags_in_artists_tags_tag_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags_in_artists
    ADD CONSTRAINT tags_in_artists_tags_tag_id_fk FOREIGN KEY (tag_id) REFERENCES public.tags(tag_id) ON DELETE RESTRICT;


--
-- TOC entry 3396 (class 2606 OID 106826)
-- Name: tags_in_playlists tags_in_playlists_playlists_playlist_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags_in_playlists
    ADD CONSTRAINT tags_in_playlists_playlists_playlist_id_fk FOREIGN KEY (playlist_id) REFERENCES public.playlists(playlist_id);


--
-- TOC entry 3397 (class 2606 OID 106831)
-- Name: tags_in_playlists tags_in_playlists_tags_tag_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags_in_playlists
    ADD CONSTRAINT tags_in_playlists_tags_tag_id_fk FOREIGN KEY (tag_id) REFERENCES public.tags(tag_id) ON DELETE RESTRICT;


--
-- TOC entry 3394 (class 2606 OID 106836)
-- Name: tags_in_songs tags_in_songs_songs_song_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags_in_songs
    ADD CONSTRAINT tags_in_songs_songs_song_id_fk FOREIGN KEY (song_id) REFERENCES public.songs(song_id);


--
-- TOC entry 3395 (class 2606 OID 106841)
-- Name: tags_in_songs tags_in_songs_tags_tag_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags_in_songs
    ADD CONSTRAINT tags_in_songs_tags_tag_id_fk FOREIGN KEY (tag_id) REFERENCES public.tags(tag_id) ON DELETE RESTRICT;


-- Completed on 2022-07-28 11:17:04

--
-- PostgreSQL database dump complete
--

