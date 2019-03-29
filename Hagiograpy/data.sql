--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.10
-- Dumped by pg_dump version 9.6.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: _images_numeriques; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._images_numeriques (
    idimage integer,
    lien_ark_gallica text,
    legende_image text,
    idoeuvre integer
);


ALTER TABLE public._images_numeriques OWNER TO rebasedata;

--
-- Name: _institution; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._institution (
    idinstitution integer,
    nom_institution text,
    localisation_idlocalisation integer
);


ALTER TABLE public._institution OWNER TO rebasedata;

--
-- Name: _jointure_manuscrit_realisation; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._jointure_manuscrit_realisation (
    manuscrit_idmanuscrit integer,
    realisation_idrealisation integer
);


ALTER TABLE public._jointure_manuscrit_realisation OWNER TO rebasedata;

--
-- Name: _jointure_oeuvre_realisation; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._jointure_oeuvre_realisation (
    realisation_idrealisation integer,
    oeuvre_idoeuvre integer
);


ALTER TABLE public._jointure_oeuvre_realisation OWNER TO rebasedata;

--
-- Name: _jointure_saint_oeuvre; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._jointure_saint_oeuvre (
    saint_idsaint integer,
    oeuvre_idoeuvre integer
);


ALTER TABLE public._jointure_saint_oeuvre OWNER TO rebasedata;

--
-- Name: _localisation; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._localisation (
    idlocalisation integer,
    ville text
);


ALTER TABLE public._localisation OWNER TO rebasedata;

--
-- Name: _manuscrit; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._manuscrit (
    idmanuscrit integer,
    cote text,
    titre text,
    nb_feuillets text,
    provenance text,
    support text,
    hauteur text,
    largeur text,
    institution_idinstitution integer
);


ALTER TABLE public._manuscrit OWNER TO rebasedata;

--
-- Name: _oeuvre; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._oeuvre (
    idoeuvre integer,
    titre text,
    auteur text,
    langue text,
    incipit text,
    explicit text,
    folios text,
    url text,
    iiif text
);


ALTER TABLE public._oeuvre OWNER TO rebasedata;

--
-- Name: _realisation; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._realisation (
    idrealisation integer,
    date_production text,
    lieu_production text,
    copiste text
);


ALTER TABLE public._realisation OWNER TO rebasedata;

--
-- Name: _saint; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._saint (
    idsaint integer,
    nom_saint text,
    biographie text
);


ALTER TABLE public._saint OWNER TO rebasedata;

--
-- Name: _user; Type: TABLE; Schema: public; Owner: rebasedata
--

CREATE TABLE public._user (
    user_id integer,
    user_nom text,
    user_login text,
    user_email text,
    user_password text
);


ALTER TABLE public._user OWNER TO rebasedata;

--
-- Data for Name: _images_numeriques; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._images_numeriques (idimage, lien_ark_gallica, legende_image, idoeuvre) FROM stdin;
1	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f99/full/full/0/native.jpg	BNF, Français 412, f. 45r. - Vie de saint Philippe	1
2	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f100/full/full/0/native.jpg	BNF, Français 412, f. 45v. - Vie de saint Philippe ; Vie de saint Jacques le Mineur	1
3	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f101/full/full/0/native.jpg	BNF, Français 412, f. 46r. - Vie de saint Jacques le Mineur	2
4	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f102/full/full/0/native.jpg	BNF, Français 412, f. 46v. - Vie de saint Jacques le Mineur	2
5	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f458/full/full/0/native.jpg	BNF, Français 412, f. 224v. - Vie de sainte Euphrasie	3
6	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f459/full/full/0/native.jpg	BNF, Français 412, f. 225r. - Vie de sainte Euphrasie	3
7	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f460/full/full/0/native.jpg	BNF, Français 412, f. 225v. - Vie de sainte Euphrasie	3
8	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f437/full/full/0/native.jpg	BNF, Français 412, f. 214r. - Vie de sainte Pélagie	4
9	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f438/full/full/0/native.jpg	BNF, Français 412, f. 214v. - Vie de sainte Pélagie	4
10	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f439/full/full/0/native.jpg	BNF, Français 412, f. 215r. - Vie de sainte Pélagie	4
11	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f435/full/full/0/native.jpg	BNF, Français 412, f. 213r. - Vie de sainte Marguerite	5
12	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f436/full/full/0/native.jpg	BNF, Français 412, f. 213v. - Vie de sainte Marguerite	5
13	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f437/full/full/0/native.jpg	BNF, Français 412, f. 214r. - Vie de sainte Marguerite	5
14	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f151/full/full/0/native.jpg	BNF, Français 412, f. 71r. - Vie de sainte Lucie	6
15	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f152/full/full/0/native.jpg	BNF, Français 412, f. 71v. - Vie de sainte Lucie	6
16	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f153/full/full/0/native.jpg	BNF, Français 412, f. 72r. - Vie de sainte Lucie	6
17	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f154/full/full/0/native.jpg	BNF, Français 412, f. 72v. - Vie de sainte Lucie	6
18	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f183/full/full/0/native.jpg	BNF, Français 412, f. 87r. - Vie de saint Sixte	7
19	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f184/full/full/0/native.jpg	BNF, Français 412, f. 87v. - Vie de saint Sixte	7
20	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f185/full/full/0/native.jpg	BNF, Français 412, f. 88r. - Vie de saint Sixte	7
21	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f186/full/full/0/native.jpg	BNF, Français 412, f. 88v. - Vie de saint Sixte	7
22	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f111/full/full/0/native.jpg	BNF, Français 412, f. 51r. - Vie de saint Longin	8
23	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f112/full/full/0/native.jpg	BNF, Français 412, f. 51v. - Vie de saint Longin	8
24	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f113/full/full/0/native.jpg	BNF, Français 412, f. 52r. - Vie de saint Longin	8
25	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f114/full/full/0/native.jpg	BNF, Français 412, f. 52v. - Vie de saint Longin	8
26	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84526286/f288/full/full/0/native.jpg	BM de Valenciennes, Ms 150, f. 141v. - Séquence de sainte Eulalie	9
\.


--
-- Data for Name: _institution; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._institution (idinstitution, nom_institution, localisation_idlocalisation) FROM stdin;
1	Bibliothèque nationale de France, Département des manuscrits	1
2	Bibliothèque municipale de Valenciennes	2
\.


--
-- Data for Name: _jointure_manuscrit_realisation; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._jointure_manuscrit_realisation (manuscrit_idmanuscrit, realisation_idrealisation) FROM stdin;
1	1
2	2
\.


--
-- Data for Name: _jointure_oeuvre_realisation; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._jointure_oeuvre_realisation (realisation_idrealisation, oeuvre_idoeuvre) FROM stdin;
1	1
1	2
1	3
2	4
1	5
1	6
1	7
1	8
1	9
\.


--
-- Data for Name: _jointure_saint_oeuvre; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._jointure_saint_oeuvre (saint_idsaint, oeuvre_idoeuvre) FROM stdin;
1	1
2	5
3	6
4	7
5	3
6	8
7	9
8	2
9	4
\.


--
-- Data for Name: _localisation; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._localisation (idlocalisation, ville) FROM stdin;
1	Paris (France)
2	Valenciennes (France)
\.


--
-- Data for Name: _manuscrit; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._manuscrit (idmanuscrit, cote, titre, nb_feuillets, provenance, support, hauteur, largeur, institution_idinstitution) FROM stdin;
1	Français 412	Recueil de textes , Vie de saints	245 feuillets + 3 gardes		Parchemin	330	245	1
2	Ms 150		443		Parchemin	237	150	2
\.


--
-- Data for Name: _oeuvre; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._oeuvre (idoeuvre, titre, auteur, langue, incipit, explicit, folios, url, iiif) FROM stdin;
1	Vie de saint Philippe	Anonyme	oil-français	Si comme la devine page tesmoigne xx ans apres l'acension Nostre Seigneur	biau miracle fait nostre sires en terre por elles et lor ames sont en pardurable gloire ensamble o le seint apostre Et la noz doinst parvenir cil qi vit (+ doxologie)	ff. 45r. - 45v.	https://gallica.bnf.fr/ark:/12148/btv1b84259980/f99	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f99/info.json
2	Vie de saint Longin	Anonyme	oil-français	Au tens ke Nostre Sires Jhesucris fu mis en crois estoit un chevalier qui Longins avoit nom. Il par le commandement Pilate feri Nostre Sires	A donc fu l'ame del saint martyr en paradiz, portee avec la compaignie des angeles, ou Dex noz doinst parvenir qil vit et regne el siecle de toz siecles. Amen.	ff. 51r. - 52v.	https://gallica.bnf.fr/ark:/12148/btv1b84259980/f111	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f111/info.json
3	Vie de sainte Marguerite	Anonyme	oil-français	Apres la glorieuse resurrection Nostre Signor Jesu Crist et puis qe si apostre orent tuit receu la celestiel corone par la victoire de martyre	ceste Marine qui fu martyriee en la cite d'Antioche est apelee seinte Marguerite.	ff. 213r. - 214r.	https://gallica.bnf.fr/ark:/12148/btv1b84259980/f435	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f435/info.json
4	Séquence de sainte Eulalie	Anonyme	ancien français	Buona pulcella fut Eulalia. Bel auret corps bellezour anima. 	Post la mort & a[ ]lui nos laist uenir. Par souue clementia.	141v	https://gallica.bnf.fr/ark:/12148/btv1b84526286/f288	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84526286/f288/info.json
5	Vie de saint Jacques le Mineur	Anonyme	oil-français	Ne voz doit mie anoier se je vous conte ici apres la vie et la passion de monsigneur seint Jaque le petit	gloire par toz les siecles des siecles. Amen.	ff. 45v. - 46v.	https://gallica.bnf.fr/ark:/12148/btv1b84259980/f100	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f100/info.json
6	Vie de sainte Euphrasie	Anonyme	oil-français	A rome ot un senat qui ot non Antigonus et estoit molt boens hom et cremoit molt Nostre Seigneur	voiz ici ton loier ici seras toz jorz mes ceste vision vit l'abeese la nuit et l'endemein morut eufrase et nostre sires li rendi la corone es cieuls que ele avoit deservie en terre	ff. 224v.- 225v.	https://gallica.bnf.fr/ark:/12148/btv1b84259980/f458	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f458/info.json
7	Vie de sainte Pélagie	Anonyme	oil-français	Nous devons tos jors rendre graces a Nostre Seignor qi ne veut pas qe li pecheor perissent	et qant ele fu trespassee cil qui l'ensevelirent aperçurent qe ce estoit feme et loerent et gloirefierent nostre signor qi avoit done a feme si grant vertu de si grant abstinence	ff. 214r. - 215r.	https://gallica.bnf.fr/ark:/12148/btv1b84259980/f437	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f437/info.json
8	Vie de sainte Luce (ou Lucie)	Anonyme	oil-français	Au jour que la renommee et la parole croissoit et enforçoit rudement par pluseurs contrees des halz miracles que Damlediex demoutroit et faisoit en la cite de Cathenense	et en cel meisme leu li fist l'en faire une mout bele eglyse ou ses orisons sont encore et seront toz tens tant com li siecles duerra	ff. 71r. - 72v.	https://gallica.bnf.fr/ark:/12148/btv1b84259980/f151	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f151/info.json
9	Vie de saint Sixte	Anonyme	oil-français	Ce fu el temps que Decius Cesar fu emperieres que cil qui NS apeloient estoient martirié et soufroient griez tourmens pour l'amour de lui	et la enfoirent il en cel meisme jor seint Felice et saint Agapite qi furent seint martyr et si sont en joie pardurable ou Nostre Sires Jesu Criz nos otroit parvenir (+ doxologie)	ff. 87r. - 88v.	https://gallica.bnf.fr/ark:/12148/btv1b84259980/f183	https://gallica.bnf.fr/iiif/ark:/12148/btv1b84259980/f183/info.json
\.


--
-- Data for Name: _realisation; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._realisation (idrealisation, date_production, lieu_production, copiste) FROM stdin;
1	1285	France (Nord ; Cambrai ?)	Inconnu
2	880	Abbaye de Saint-Amand (France)	Inconnu
\.


--
-- Data for Name: _saint; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._saint (idsaint, nom_saint, biographie) FROM stdin;
1	Philippe	Philippe est un Juif helléniste faisant partie des Sept, les premiers diacres choisis par les membres de l'Église primitive de Jérusalem à l'initiative de l'assemblée des disciples et des apôtres afin d'aider ces derniers. Il ne faut pas le confondre avec l'apôtre Philippe mentionné dans les Évangiles, même si, dans la formation des légendes, les biographies des deux Philippe ont été reliées. Il a également une fonction d'évangéliste en Samarie et favorise la christianisation de l'Éthiopie. Il fait aussi partie des Septante disciples choisis par Jésus-Christ. 
2	Jacques le Mineur	Jacques d'Alphée ou Jacques, fils d'Alphée, du grec Iάκωβος ὁ τοῦ Ἁλφαίου, est un Juif de Galilée qui fait partie des douze apôtres de Jésus. Dans la tradition du christianisme occidental, il est aussi appelé Jacques le Mineur, pour le distinguer de Jacques de Zébédée, dit Jacques le Majeur, frère de l'apôtre Jean.\n\nIl est présenté comme fils d'Alphée, nom traduit du grec Alphaios, de l'araméen Alpay, lui-même parfois assimilé à Clopas[réf. nécessaire]. Selon l'Évangile de Marc (Mc 2:14), l'apôtre Lévi-Matthieu est aussi fils d'un Alphée. 
3	Euphrasie	Fille d'Antigone, gouverneur de Lycie, parente de l'empereur Théodose le Grand, elle quitta la maison paternelle pour s'enfermer dans un monastère où elle resta jusqu'à sa mort cachée sous des habits d'homme et se livrant aux pratiques les plus rigoureuses.\n\nElle est fêtée par les Grecs le 25 novembre, par les Latins le 11 février et par les Chrétiens le mars. 
4	Pélagie	Sainte Pélagie martyre à Tarse est une sainte qui a vécu au IIIe siècle. On la fête le 8 Octobre.\n\nElle aurait été fiancée à l'un des fils de l'empereur Dioclétien. Elle fut curieuse de découvrir le christianisme et, convaincue, décida de se faire baptiser. Ce faisant, elle modifia sa façon de vivre, devint modeste d'aspect et de comportement, ce qui la désigna comme chrétienne. L'empereur, furieux de ce qu'il considérait comme une traîtrise envers son milieu, et par ses attaches, la fit arrêter, enfermer et la condamna à périr dans un bœuf d'airain rougi au feu. 
5	Marguerite	Marguerite d'Antioche ou Marine d'Antioche ou sainte Marina est une vierge martyre du IVe siècle (vers 305), fêtée le 17 juillet en Orient et le 20 juillet en Occident. Elle est invoquée pour une délivrance, en particulier par les femmes enceintes parce que la légende raconte qu'elle est sortie indemne du ventre du dragon qui l'avait engloutie. À Paris, elle était vénérée dans l'église Saint-Germain-des-Prés près de laquelle la rue du Dragon garde le souvenir d'une enseigne à sa mémoire. 
6	Luce (Lucie)	Lucie de Cyrène (IVe siècle), avec Cyprille et Aroa, martyres à Cyrène en Libye ; fêtées par l'Église orthodoxe le 4 juillet et par l'Église catholique romaine localement le 5 juillet.
7	Sixte	Sixte de Reims est un évêque de Reims du IIIe siècle. Il a été proclamé saint. 
8	Longin	Longin (IVe siècle), Père du désert en Égypte célèbre pour ses apophtegmes.
9	Eulalie	Sainte Eulalie de Mérida est une vierge martyre morte en 304, célébrée dans un hymne de Prudence (Peristephanon) et dans la célèbre Séquence de sainte Eulalie, premier texte littéraire en français. 
\.


--
-- Data for Name: _user; Type: TABLE DATA; Schema: public; Owner: rebasedata
--

COPY public._user (user_id, user_nom, user_login, user_email, user_password) FROM stdin;
1	clem123	cadx33	clem-and33@hotmail.com	pbkdf2:sha256:50000$7HGFtLYp$8770a0be251cf701b7a50db2ea2370ca8c2fdd9541c9e64ec84b592825f649fb
2	test	test	corentin.faye@chartes.psl.eu	pbkdf2:sha256:50000$o7DX0jNU$5b0a6ba030917f448e5a41796f60afed51f749ee2f3f2f3989f40694f802e4c6
3	Jacquot	intaglio	olivier.jacquot@chartes.psl.eu	pbkdf2:sha256:50000$cljyYt1e$5c7743ab754e81bcf0b664c0b597523d4a2021e3c7df2584efcca1e51940599e
\.


--
-- PostgreSQL database dump complete
--

